"""
Fix Generation Component.
Responsible for generating code fixes based on context and explanations.
"""
from pydantic import BaseModel, Field
import ast
import textwrap
try:
    from .llm import LLMService
except ImportError:
    from src.llm import LLMService

class FixResponse(BaseModel):
    """Schema for the fix generation output."""
    thought_process: str = Field(..., description="Brief reasoning about what needs to be fixed.")
    code: str = Field(..., description="The complete, fully valid Python code for the fixed function/method only.")

class FixGenerator:
    """
    Generates software fixes using a source-aware prompting strategy with Structured Outputs.
    """
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        
    def generate(self, source_code: str, explanation: str, function_name: str = None) -> dict:
        """
        Generate a fix for the provided source code based on the explanation.
        
        Args:
            source_code: The original source code containing the bug
            explanation: The natural language explanation of the bug
            
        Returns:
            The fixed source code
        """
        prompt = self._build_function_prompt(source_code, explanation, function_name)
        
        # Use Structured Generation via Instructor/LLMService
        try:
            response = self.llm_service.generate_structured(prompt, FixResponse)

            raw_fix = response.code
            snippet = textwrap.dedent(response.code).strip("\n") + "\n"

            # If function_name provided, splice the function into the original module first.
            # Validate syntax on the final candidate module (not on the raw snippet), since
            # method-only code can be indented and still be valid after splicing.
            if function_name:
                try:
                    candidate = self.apply_fix(source_code, function_name, snippet)
                except Exception as e:
                    print(f"Error applying fix: {e}")
                    candidate = source_code
            else:
                candidate = snippet

            try:
                ast.parse(candidate)
            except SyntaxError as e:
                print(f"Generated code did not parse, falling back to original: {e}")
                candidate = source_code

            return {
                "code": candidate,
                "raw_fix": raw_fix,
                "thought_process": response.thought_process,
            }

        except Exception as e:
            print(f"Error in fix generation: {e}")
            return {"code": "", "raw_fix": "", "thought_process": f"Error: {e}"}


    def _build_function_prompt(self, source_code: str, explanation: str, function_name: str) -> str:
        return f"""You are an expert developer. Fix the bug in the function `{function_name}` based on the diagnosis.

[SOURCE CODE]
{source_code}

[BUG DIAGNOSIS]
{explanation}

[OUTPUT FORMAT]
Return a JSON object with exactly these keys:
- thought_process: brief summary of the fix.
- code: the complete, fully valid Python code for the fixed `{function_name}` only (including decorators if any). Do NOT include a docstring. Do NOT include Markdown fences.
"""

    def generate_direct(self, source_code: str, function_name: str) -> dict:
        """
        Generate a fix directly from source code WITHOUT an explanation.
        Used as a baseline to measure the value of explanations.
        
        Args:
            source_code: The original source code containing the bug
            function_name: The name of the function to fix
            
        Returns:
            dict with 'code', 'raw_fix', and 'thought_process'
        """
        prompt = self._build_direct_prompt(source_code, function_name)
        
        try:
            response = self.llm_service.generate_structured(prompt, FixResponse)

            raw_fix = response.code
            snippet = textwrap.dedent(response.code).strip("\n") + "\n"

            try:
                candidate = self.apply_fix(source_code, function_name, snippet)
            except Exception as e:
                print(f"Error applying fix: {e}")
                candidate = source_code

            try:
                ast.parse(candidate)
            except SyntaxError as e:
                print(f"Generated code did not parse, falling back to original: {e}")
                candidate = source_code

            return {
                "code": candidate,
                "raw_fix": raw_fix,
                "thought_process": response.thought_process,
            }

        except Exception as e:
            print(f"Error in direct fix generation: {e}")
            return {"code": "", "raw_fix": "", "thought_process": f"Error: {e}"}

    def _build_direct_prompt(self, source_code: str, function_name: str) -> str:
        """Prompt for direct fix: source code only, no explanation."""
        return f"""You are an expert developer. Fix any bugs in the function `{function_name}` in the following source code.
        
[SOURCE CODE]
{source_code}

[OUTPUT FORMAT]
Return a JSON object with exactly these keys:
- thought_process: brief summary of the fix.
- code: the complete, fully valid Python code for the fixed `{function_name}` only (including decorators if any). Do NOT include a docstring. Do NOT include Markdown fences.
"""

    def generate_direct_java(self, source_code: str, function_name: str) -> dict:
        """
        Generate a fix directly from Java source code WITHOUT an explanation.
        Used for data-contamination control (comparing Java vs Python fix success).

        Returns dict with 'raw_fix' and 'thought_process' only (no apply/validation).
        """
        prompt = self._build_direct_prompt_java(source_code, function_name)

        try:
            response = self.llm_service.generate_structured(prompt, FixResponse)
            return {
                "raw_fix": response.code,
                "thought_process": response.thought_process,
            }
        except Exception as e:
            print(f"Error in direct Java fix generation: {e}")
            return {"raw_fix": "", "thought_process": f"Error: {e}"}

    def _build_direct_prompt_java(self, source_code: str, function_name: str) -> str:
        """Prompt for direct Java fix: source code only, no explanation."""
        return f"""You are an expert developer. Fix any bugs in the function `{function_name}` in the following source code.
        
[SOURCE CODE]
{source_code}

[OUTPUT FORMAT]
Return a JSON object with exactly these keys:
- thought_process: brief summary of the fix.
- code: the complete, fully valid Java code for the fixed `{function_name}` only (including decorators if any). Do NOT include a docstring. Do NOT include Markdown fences.
"""

    def apply_fix(self, original_source: str, function_name: str, new_function_code: str) -> str:
        """
        Replace the function/method `function_name` in `original_source` with `new_function_code`.
        Preserves the rest of the file exactly.
        """
        try:
            tree = ast.parse(original_source)
            lines = original_source.splitlines()
            
            target_node = None
            parts = function_name.split(".")
            
            # Find the node
            if len(parts) == 2:
                # Class.method
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
            
            if not target_node:
                raise ValueError(f"Function {function_name} not found in source.")
                
            # Determine Indentation from Original
            # We look at the first line of the original function definition
            start_line_idx = target_node.lineno - 1
            original_line = lines[start_line_idx]
            indentation = original_line[:len(original_line) - len(original_line.lstrip())]
            
            # Prepare new lines with correct indentation
            # First dedent to remove any potential LLM-added indentation
            dedented_code = textwrap.dedent(new_function_code)
            
            new_lines = []
            for line in dedented_code.splitlines():
                if line.strip(): # Don't indent empty lines if they are empty
                     new_lines.append(indentation + line)
                else:
                    new_lines.append("")

            # Find extent of the old function including decorators
            # ast.Node lineno usually starts at the 'def', decorators are separate.
            # However, for replacement, we want to replace from the first decorator if present? 
            # Or assume the LLM outputs decorators?
            # Prompt asked for decorators.
            
            start_lineno = target_node.lineno
            if target_node.decorator_list:
                 start_lineno = target_node.decorator_list[0].lineno
            
            end_lineno = target_node.end_lineno
            
            # Splicing
            # Python lines are 1-indexed. List indices are 0-indexed.
            # Prefix: lines[:start_lineno-1]
            # Suffix: lines[end_lineno:]
            
            final_lines = lines[:start_lineno-1] + new_lines + lines[end_lineno:]
            return "\n".join(final_lines)

        except Exception as e:
            # Re-raise to be caught by caller
            raise e
