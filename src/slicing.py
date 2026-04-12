"""
Dynamic program slicing for Python code.
Supports block, backward (dynamic), forward (static), and union strategies.
"""
import sys
import os
import ast
from typing import Set, Dict, Optional
from enum import Enum


class ContextStrategy(Enum):
    """Available slicing strategies."""
    BLOCK = "block"       # Enclosing code block around failure
    BACKWARD = "backward" # Dynamic backward slice (execution history)
    FORWARD = "forward"   # Static forward slice (function-scoped)
    UNION = "union"       # Backward + Forward combined


class TraceRunner:
    """Captures execution trace by running a test file."""
    
    def __init__(self, target_file: str):
        self.target_file = os.path.abspath(target_file)
        self.executed_lines: Set[int] = set()
        self.last_executed_line: Optional[int] = None
        self.exception_line: Optional[int] = None  # Line where exception was raised
    
    def _trace_calls(self, frame, event, arg):
        if event == 'call':
            filename = os.path.abspath(frame.f_code.co_filename)
            if filename == self.target_file:
                return self._trace_lines
        return self._trace_calls

    def _trace_lines(self, frame, event, arg):
        if event == 'line':
            self.executed_lines.add(frame.f_lineno)
            self.last_executed_line = frame.f_lineno
        elif event == 'exception':
            # Only capture the FIRST exception (deepest in call stack)
            # This ensures we get the actual failure location, not the call site
            if self.exception_line is None:
                self.exception_line = frame.f_lineno
        return self._trace_lines

    def run_wrapper(self, test_script_path: str):
        """Execute test script and capture execution trace.
        
        Uses importlib + unittest.TestLoader to properly run tests instead of exec(),
        which doesn't properly discover/run unittest tests.
        """
        import importlib.util
        import unittest
        import io
        
        self.executed_lines.clear()
        self.last_executed_line = None
        self.exception_line = None
        original_trace = sys.gettrace()
        test_dir = os.path.dirname(test_script_path)
        parent_dir = os.path.dirname(test_dir)
        
        # Add both test directory and parent to path for imports
        added_paths = []
        for path in [test_dir, parent_dir]:
            if path and path not in sys.path:
                sys.path.insert(0, path)
                added_paths.append(path)
        
        try:
            # Load the test module properly using importlib
            spec = importlib.util.spec_from_file_location('test_module', test_script_path)
            test_module = importlib.util.module_from_spec(spec)
            
            # Set up tracer before executing module
            sys.settrace(self._trace_calls)
            spec.loader.exec_module(test_module)
            
            # Run the tests using unittest.TestLoader
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(test_module)
            
            # Run silently (suppress output)
            runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
            runner.run(suite)
            
        except SystemExit:
            pass
        except Exception:
            # We expect tests to fail during slicing (that's why we're slicing)
            pass
        finally:
            sys.settrace(original_trace)
            for path in added_paths:
                if path in sys.path:
                    sys.path.remove(path)


class DependencyAnalyzer(ast.NodeVisitor):
    """Analyzes variable definitions, usages, and control dependencies in source code."""
    
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tree = ast.parse(source_code)
        self.definitions: Dict[int, Set[str]] = {}
        self.usages: Dict[int, Set[str]] = {}
        self.control_dependencies: Dict[int, int] = {}
        self.analyze()

    def analyze(self):
        self._analyze_node(self.tree, None)

    def _analyze_node(self, node: ast.AST, current_control_line: Optional[int]):
        if hasattr(node, 'lineno') and current_control_line is not None:
            self.control_dependencies[node.lineno] = current_control_line

        if isinstance(node, ast.Name) and hasattr(node, 'lineno'):
            if isinstance(node.ctx, ast.Store):
                self._add_def(node.lineno, node.id)
            elif isinstance(node.ctx, ast.Load):
                self._add_use(node.lineno, node.id)
        elif isinstance(node, ast.Attribute) and hasattr(node, 'lineno'):
            # Track attribute access like self._foo as "self._foo"
            if isinstance(node.value, ast.Name):
                attr_name = f"{node.value.id}.{node.attr}"
                if isinstance(node.ctx, ast.Store):
                    self._add_def(node.lineno, attr_name)
                elif isinstance(node.ctx, ast.Load):
                    self._add_use(node.lineno, attr_name)
        elif isinstance(node, ast.arg) and hasattr(node, 'lineno'):
            self._add_def(node.lineno, node.arg)
        
        next_control = current_control_line
        if isinstance(node, (ast.If, ast.While, ast.For, ast.FunctionDef, ast.AsyncFunctionDef)):
            if hasattr(node, 'lineno'):
                next_control = node.lineno
        
        for child in ast.iter_child_nodes(node):
            self._analyze_node(child, next_control)

    def _add_def(self, line: int, var_name: str):
        if line not in self.definitions:
            self.definitions[line] = set()
        self.definitions[line].add(var_name)

    def _add_use(self, line: int, var_name: str):
        if line not in self.usages:
            self.usages[line] = set()
        self.usages[line].add(var_name)

    def get_backward_slice(self, executed_lines: Set[int], seed_line: int) -> Set[int]:
        """Compute dynamic backward slice from seed_line using execution history."""
        slice_lines = {seed_line}
        needed_vars = set()
        
        if seed_line in self.usages:
            needed_vars.update(self.usages[seed_line])
        if seed_line in self.control_dependencies:
            slice_lines.add(self.control_dependencies[seed_line])
        
        sorted_executed = sorted([l for l in executed_lines if l <= seed_line], reverse=True)
        
        changed = True
        while changed:
            changed = False
            for line in sorted_executed:
                is_in_slice = (line in slice_lines)
                if not is_in_slice and line in self.definitions:
                    if not self.definitions[line].isdisjoint(needed_vars):
                        is_in_slice = True
                
                if is_in_slice:
                    if line not in slice_lines:
                        slice_lines.add(line)
                        changed = True
                    if line in self.usages:
                        new_needs = self.usages[line] - needed_vars
                        if new_needs:
                            needed_vars.update(new_needs)
                            changed = True
                    if line in self.control_dependencies:
                        ctrl = self.control_dependencies[line]
                        if ctrl not in slice_lines:
                            slice_lines.add(ctrl)
                            changed = True
        return slice_lines

    def get_forward_slice(self, seed_line: int) -> Set[int]:
        """
        Compute static forward slice from seed_line, bounded to enclosing function.
        This prevents 'taint explosion' where variables propagate across the entire class.
        """
        slice_lines = set()
        tracked_vars = set()

        # Find the enclosing function scope (tightest match for nested functions)
        scope_start = 0
        scope_end = float('inf')
        
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                start = node.lineno
                end = getattr(node, 'end_lineno', 999999)
                
                if start <= seed_line <= end:
                    if (end - start) < (scope_end - scope_start):
                        scope_start = start
                        scope_end = end
        
        # Track variables at the seed line
        if seed_line in self.definitions:
            tracked_vars.update(self.definitions[seed_line])
        if seed_line in self.usages:
            tracked_vars.update(self.usages[seed_line])
        
        # Scan forward within scope
        all_lines = sorted(list(set(self.usages.keys()) | set(self.definitions.keys())))
        forward_lines = [l for l in all_lines if l > seed_line and scope_start <= l <= scope_end]
        
        for line in forward_lines:
            line_uses = self.usages.get(line, set())
            if not tracked_vars.isdisjoint(line_uses):
                slice_lines.add(line)
                # Transitive taint: track newly defined variables
                if line in self.definitions:
                    tracked_vars.update(self.definitions[line])
        
        return slice_lines


def format_context(source_code: str, relevant_lines: Set[int]) -> str:
    """Format selected lines with line numbers."""
    lines = source_code.splitlines()
    output = []
    sorted_lines = sorted(list(relevant_lines))
    
    for line_num in sorted_lines:
        if 0 <= line_num - 1 < len(lines):
            code = lines[line_num - 1].rstrip()
            output.append(f"{line_num:4d} | {code}")
            
    return "\n".join(output)


def get_enclosing_block(source_code: str, failure_line: int) -> Set[int]:
    """
    Extract the innermost code block containing the failure line.
    
    A code block is defined as a compound statement (function, loop, conditional, etc.)
    that contains the failure line.
    
    Args:
        source_code: The source code as a string
        failure_line: The line number where the failure occurred
    
    Returns:
        Set of line numbers making up the enclosing block
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return {failure_line}
    
    # Find all compound statements containing the failure line
    candidates = []
    for node in ast.walk(tree):
        # Compound statements that define code blocks
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef,
                             ast.For, ast.AsyncFor, ast.While, 
                             ast.If, ast.With, ast.AsyncWith, ast.Try)):
            if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
                if node.lineno <= failure_line <= node.end_lineno:
                    candidates.append((node.lineno, node.end_lineno, type(node).__name__))
    
    if not candidates:
        # No enclosing block found, return just the failure line
        return {failure_line}
    
    # Sort by size (smallest first = innermost block)
    candidates.sort(key=lambda x: x[1] - x[0])
    start, end, _ = candidates[0]
    
    return set(range(start, end + 1))


def _compute_slice_lines(source_file: str, test_file: str, strategy: str = "union") -> tuple[Set[int], str]:
    """
    Internal function to compute slice lines and read source code.
    
    Args:
        source_file: Path to the source file containing the defect
        test_file: Path to the test file that triggers the failure
        strategy: One of 'block', 'backward', 'forward', 'union' (default: union)
    
    Returns:
        Tuple of (set of line numbers, source_code string)
        Returns (empty set, error message) if trace capture fails
    """
    tracer = TraceRunner(source_file)
    tracer.run_wrapper(test_file)
    
    if not tracer.executed_lines:
        return set(), "Error: No execution trace captured."
    
    # Prefer exception_line (actual failure point), fallback to last_executed_line
    failure_line = tracer.exception_line or tracer.last_executed_line
    if not failure_line:
        failure_line = max(tracer.executed_lines)

    with open(source_file, 'r') as f:
        source_code = f.read()

    final_lines: Set[int] = set()
    
    if strategy == "block":
        # Extract the innermost enclosing code block
        final_lines = get_enclosing_block(source_code, failure_line)
    else:
        analyzer = DependencyAnalyzer(source_code)
        # Backward slice is the foundation for all non-block strategies
        backward_lines = analyzer.get_backward_slice(tracer.executed_lines, failure_line)
        
        if strategy == "backward":
            final_lines = backward_lines
        elif strategy == "forward":
            forward_lines = analyzer.get_forward_slice(failure_line)
            final_lines = forward_lines
        elif strategy == "union":
            forward_lines = analyzer.get_forward_slice(failure_line)
            final_lines = backward_lines.union(forward_lines)

    return final_lines, source_code


def get_context(source_file: str, test_file: str, strategy: str = "union") -> str:
    """
    Generate relevant code context using the specified slicing strategy.
    
    Args:
        source_file: Path to the source file containing the defect
        test_file: Path to the test file that triggers the failure
        strategy: One of 'block', 'backward', 'forward', 'union' (default: union)
    
    Returns:
        Formatted code slice with line numbers
    """
    final_lines, source_code = _compute_slice_lines(source_file, test_file, strategy)
    
    if not final_lines and source_code.startswith("Error:"):
        return source_code
    
    return format_context(source_code, final_lines)


def get_context_with_lines(source_file: str, test_file: str, strategy: str = "union") -> tuple[str, Set[int]]:
    """
    Generate relevant code context and return the raw line numbers.
    
    Args:
        source_file: Path to the source file containing the defect
        test_file: Path to the test file that triggers the failure
        strategy: One of 'block', 'backward', 'forward', 'union' (default: union)
    
    Returns:
        Tuple of (formatted_context, set of line numbers in the slice)
    """
    final_lines, source_code = _compute_slice_lines(source_file, test_file, strategy)
    
    if not final_lines and source_code.startswith("Error:"):
        return source_code, set()
    
    return format_context(source_code, final_lines), final_lines


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python slicing.py <source> <test> <strategy: block|backward|forward|union>")
        sys.exit(1)
    
    print(get_context(sys.argv[1], sys.argv[2], sys.argv[3]))
