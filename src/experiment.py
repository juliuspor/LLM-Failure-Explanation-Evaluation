"""
Unified experiment runner with composable context levels.
"""
import ast
import os
from enum import Flag, auto
from typing import Optional, Dict, Set

from .slicing import get_context, get_context_with_lines
from pydantic import BaseModel, Field

CRITERIA_INSTRUCTIONS = """
Your explanation should NOT:
- Use jargon or complex language that obscures the issue
- Leave the developer guessing about the root cause
- Omit what happened, why it happened, or where it occurred
- Suggest fixes that are vague or lack a list of steps
- Fail to reference specific variable names, method names, or line numbers from the code
- Include unnecessary filler or redundant information
"""

OUTPUT_FORMAT_INSTRUCTIONS = """
[OUTPUT FORMAT]
Return ONLY a valid JSON object with exactly this key:
{"explanation": "..."}

Rules:
- Output exactly one top-level JSON object (no surrounding text).
- Use exactly the key "explanation" (no extra keys).
- The value must be a valid JSON string. If you need newlines, write "\\n" inside the string (do not include literal newlines).
- Do not wrap the JSON in Markdown fences.
"""


class ExplanationResponse(BaseModel):
    explanation: str = Field(..., description="Plain-text explanation of why the code fails.")


class ContextLevel(Flag):
    """
    Bitflag for composable context levels.
    
    Levels can be combined with bitwise OR:
        ContextLevel.CODE | ContextLevel.ERROR | ContextLevel.SLICE_BACKWARD
    """
    NONE = 0
    CODE = auto()
    ERROR = auto()
    TEST = auto()
    DOCSTRING = auto()
    SLICE_BLOCK = auto()
    SLICE_BACKWARD = auto()
    SLICE_FORWARD = auto()
    SLICE_UNION = auto()


# Mapping from ContextLevel slice flags to slicing strategy names
_SLICE_STRATEGY_MAP = {
    ContextLevel.SLICE_BLOCK: "block",
    ContextLevel.SLICE_BACKWARD: "backward",
    ContextLevel.SLICE_FORWARD: "forward",
    ContextLevel.SLICE_UNION: "union",
}


def parse_levels(levels_str: str) -> ContextLevel:
    """
    Parse comma-separated level names into ContextLevel flags.
    
    Args:
        levels_str: Comma-separated level names (e.g., "CODE,ERROR,TEST")
    
    Returns:
        Combined ContextLevel flags
    """
    result = ContextLevel.NONE
    for name in levels_str.upper().split(","):
        name = name.strip()
        try:
            result |= ContextLevel[name]
        except KeyError:
            raise ValueError(f"Unknown context level: {name}. Valid: {[l.name for l in ContextLevel if l != ContextLevel.NONE]}")
    return result


class Experiment:
    """
    Unified experiment runner with isolated, composable context levels.
    
    Usage:
        exp = Experiment(defect)
        prompt = exp.get_prompt(ContextLevel.CODE | ContextLevel.ERROR)
        result = exp.run(ContextLevel.CODE | ContextLevel.ERROR, llm_service)
    """
    
    def __init__(self, defect: dict):
        """
        Initialize experiment with a Python defect definition.
        
        Args:
            defect: Dict with keys: source_path, test_path, error, ground_truth
        """
        self.defect = defect
        self._source_code: Optional[str] = None
        self._slices: Dict[ContextLevel, str] = {}
        self._slice_lines: Dict[ContextLevel, Set[int]] = {}
    
    @property
    def source_code(self) -> str:
        """Lazy-load source code."""
        if self._source_code is None:
            with open(self.defect["source_path"], "r") as f:
                self._source_code = f.read()
        return self._source_code
    
    def _read_test_file(self) -> str:
        """Read the test file content from test_path."""
        try:
            with open(self.defect['test_path'], 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Test file not found: {self.defect['test_path']}")
    
    def get_function_code(self) -> str:
        """
        Extract the function/method code specified in defect's function_name.
        Excludes the docstring.
        
        Raises:
            ValueError: If function_name is missing or function not found
        """
        function_name = self.defect.get("function_name")
        if not function_name:
            raise ValueError("defect must have 'function_name' to use CODE context")
        
        parts = function_name.split(".")
        tree = ast.parse(self.source_code)
        lines = self.source_code.splitlines()
        
        target_node = None
        
        if len(parts) == 2:
            # Class.method format
            class_name, method_name = parts
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == class_name:
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == method_name:
                            target_node = item
                            break
        else:
            # Top-level function
            func_name = parts[0]
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func_name:
                    target_node = node
                    break
        
        if target_node is None:
            raise ValueError(f"Function '{function_name}' not found in source file")
        
        # Get line range (1-indexed)
        start_line = target_node.lineno
        end_line = target_node.end_lineno
        
        # Skip docstring if present
        if (target_node.body and 
            isinstance(target_node.body[0], ast.Expr) and 
            isinstance(target_node.body[0].value, ast.Constant) and 
            isinstance(target_node.body[0].value.value, str)):
            docstring_end = target_node.body[0].end_lineno
            # Include function signature, skip docstring, include rest
            signature_lines = lines[start_line - 1 : target_node.body[0].lineno - 1]
            body_lines = lines[docstring_end : end_line]
            return "\n".join(signature_lines + body_lines)
        
        # No docstring, return entire function
        return "\n".join(lines[start_line - 1 : end_line])

    
    def get_slice(self, slice_level: ContextLevel) -> str:
        """
        Get slice for a specific slice level (lazy-computed and cached).
        
        Args:
            slice_level: One of SLICE_BLOCK, SLICE_BACKWARD, SLICE_FORWARD, SLICE_UNION
        """
        if slice_level not in _SLICE_STRATEGY_MAP:
            raise ValueError(f"Invalid slice level: {slice_level}")
        
        if slice_level not in self._slices:
            strategy = _SLICE_STRATEGY_MAP[slice_level]
            formatted_context, line_numbers = get_context_with_lines(
                self.defect["source_path"],
                self.defect["test_path"],
                strategy=strategy
            )
            self._slices[slice_level] = formatted_context
            self._slice_lines[slice_level] = line_numbers
        return self._slices[slice_level]
    
    def get_slice_lines(self, slice_level: ContextLevel) -> Set[int]:
        """
        Get raw line numbers for a specific slice level.
        
        Ensures the slice is computed first (lazy computation).
        
        Args:
            slice_level: One of SLICE_BLOCK, SLICE_BACKWARD, SLICE_FORWARD, SLICE_UNION
        
        Returns:
            Set of line numbers (1-indexed) included in the slice
        """
        if slice_level not in _SLICE_STRATEGY_MAP:
            raise ValueError(f"Invalid slice level: {slice_level}")
        
        # Ensure slice is computed (this populates _slice_lines)
        if slice_level not in self._slice_lines:
            self.get_slice(slice_level)
        
        return self._slice_lines.get(slice_level, set())
    
    def get_docstring(self) -> Optional[str]:
        """
        Extract docstring from the function specified in defect's function_name.
        
        Returns:
            The function's docstring, or None if not found
        """
        function_name = self.defect.get("function_name")
        if not function_name:
            return None
        
        # Parse: "ClassName.method_name" or just "function_name"
        parts = function_name.split(".")
        
        try:
            tree = ast.parse(self.source_code)
        except SyntaxError:
            return None
        
        # Find the function/method
        if len(parts) == 2:
            # Class.method format
            class_name, method_name = parts
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == class_name:
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == method_name:
                            return ast.get_docstring(item)
        else:
            # Top-level function
            func_name = parts[0]
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func_name:
                    return ast.get_docstring(node)
        
        return None
    
    def get_prompt(self, levels: ContextLevel) -> str:
        """
        Build prompt from selected context levels.
        
        Args:
            levels: Bitwise OR of ContextLevel flags to include
        
        Returns:
            Formatted prompt string with selected context sections
        """
        if levels == ContextLevel.NONE:
            raise ValueError("At least one context level must be specified")
        
        prompt = "Explain why this code fails.\n\n"
        prompt += OUTPUT_FORMAT_INSTRUCTIONS.strip() + "\n\n"
        
        # Add sections in consistent order
        if ContextLevel.CODE in levels:
            prompt += f"[CODE]\n{self.get_function_code()}\n\n"
        
        if ContextLevel.ERROR in levels:
            prompt += f"[ERROR]\n{self.defect['error']}\n\n"
        
        if ContextLevel.TEST in levels:
            test_content = self._read_test_file()
            prompt += f"[TEST]\n{test_content}\n\n"
        
        if ContextLevel.DOCSTRING in levels:
            docstring = self.get_docstring()
            if docstring:
                prompt += f"[DOCSTRING]\n{docstring}\n\n"
        
        # Handle slices (only one slice type per prompt makes sense)
        for slice_level, strategy_name in _SLICE_STRATEGY_MAP.items():
            if slice_level in levels:
                slice_content = self.get_slice(slice_level)
                prompt += f"[SLICE_{strategy_name.upper()}]\n{slice_content}\n\n"
        
        prompt += CRITERIA_INSTRUCTIONS
        return prompt
    
    def run(self, levels: ContextLevel, llm_service) -> str:
        """
        Execute experiment with specified context levels.
        
        Args:
            levels: Context levels to include in prompt
            llm_service: LLMService instance for generation
        
        Returns:
            LLM-generated explanation
        """
        prompt = self.get_prompt(levels)
        response = llm_service.generate_structured(prompt, ExplanationResponse)
        return response.explanation
    
    @staticmethod
    def levels_to_string(levels: ContextLevel) -> str:
        """Convert context levels to a readable string identifier."""
        parts = []
        for level in ContextLevel:
            if level.name != "NONE" and level in levels:
                parts.append(level.name)
        
        # specific check for baseline (all 8 levels)
        if len(parts) == 8:
            return "BASELINE"
            
        return "_".join(parts) if parts else "NONE"
