"""
Patching Validator Module.
Validates fix snippets by patching them into original source modules before running tests.
"""
import subprocess
import tempfile
import shutil
import os
import sys
import re


# Mapping of defect IDs to their patching configuration
PATCH_CONFIG = {
    "defect1": {
        "source_path": "failures/python_defects/hit01_timezone.py",
        "module_name": "hit01_timezone",
        "function_name": "for_offset_hours_minutes",
        "class_name": "DateTimeZone",
        "start_marker": "def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int)",
        "end_marker": "def for_offset_millis(cls, millis_offset: int)",
    },
    "defect2": {
        "source_path": "failures/python_defects/hit02_grayscale.py",
        "module_name": "hit02_grayscale",
        "function_name": "get_paint",
        "class_name": "GrayPaintScale",
        # Use the docstring start to uniquely identify this get_paint (vs the abstract one)
        "start_marker": "Returns a paint (RGB tuple) for the specified value.",
        "end_marker": "def __eq__(self, other)",
        "start_offset": -3,  # Go back 3 lines from docstring to method def
    },
    "defect3": {
        "source_path": "failures/python_defects/hit03_translator.py",
        "module_name": "hit03_translator",
        "function_name": "translate",
        "class_name": "CharSequenceTranslator",
        "start_marker": "def translate(self, input_seq: Optional[str], out: List[int])",
        "end_marker": "def with_translators(self",
    },
    "defect4": {
        "source_path": "failures/python_defects/hit04_timeperiod.py",
        "module_name": "hit04_timeperiod",  # Must match what test file imports
        "function_name": "_update_bounds",
        "class_name": "TimePeriodValues",
        "start_marker": "def _update_bounds(self, period: TimePeriod, index: int)",
        "end_marker": "def _recalculate_bounds(self)",
        "env_vars": {"TEST_MODULE": "hit04_timeperiod"},  # Set env for test
    },
    "defect5": {
        "source_path": "failures/python_defects/hit05_arrayutils.py",
        "module_name": "hit05_arrayutils",
        "function_name": "add",
        "class_name": "ArrayUtils",
        # Use specific signature to distinguish from add_all and add_at_index
        "start_marker": "def add(array: Optional[List[T]], element: T, expected_type:",
        "end_marker": "def add_at_index(array:",
    },
    "defect6": {
        "source_path": "failures/python_defects/hit06_codeconsumer.py",
        "module_name": "hit06_codeconsumer",
        "function_name": "add_number",
        "class_name": "CodeConsumer",
        "start_marker": "def add_number(self, x: float):",
        "end_marker": "@staticmethod",  # is_negative_zero follows add_number
    },
    "defect7": {
        "source_path": "failures/python_defects/hit07_classutils.py",
        "module_name": "hit07_classutils",
        "function_name": "to_class",
        "class_name": "ClassUtils",
        "start_marker": "def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:",
        "end_marker": "# Short canonical name",
    },
    "defect8": {
        "source_path": "failures/python_defects/hit08_locale.py",
        "module_name": "hit08_locale",
        "function_name": "to_locale",
        "class_name": "LocaleUtils",
        "start_marker": "def to_locale(cls, locale_str: str) -> Optional[Locale]:",
        "end_marker": "# -----------------------------------------------------------------------",
    },
    "defect9": {
        "source_path": "failures/python_defects/hit09_stringutils.py",
        "module_name": "hit09_stringutils",
        "function_name": "replace_each",
        "class_name": "StringUtils",
        "start_marker": "def replace_each(",
        "end_marker": "__PATCH_END__",
        "start_offset": -1,  # include @staticmethod
    },
    "defect10": {
        "source_path": "failures/python_defects/hit10_numberutils.py",
        "module_name": "hit10_numberutils",
        "function_name": "create_number",
        "class_name": "NumberUtils",
        "start_marker": "def create_number(",
        "end_marker": "__PATCH_END__",
        "start_offset": -1,  # include @staticmethod
    },
    "defect11": {
        "source_path": "failures/python_defects/hit11_randomstringutils.py",
        "module_name": "hit11_randomstringutils",
        "function_name": "random",
        "class_name": "RandomStringUtils",
        "start_marker": "def random(",
        "end_marker": "__PATCH_END__",
        "start_offset": -1,  # include @staticmethod
    },
    "defect12": {
        "source_path": "failures/python_defects/hit12_wordutils.py",
        "module_name": "hit12_wordutils",
        "function_name": "abbreviate",
        "class_name": "WordUtils",
        "start_marker": "def abbreviate(",
        "end_marker": "__PATCH_END__",
        "start_offset": -1,  # include @staticmethod
    },
}


class PatchingValidator:
    """
    Validates a fix snippet by patching it into the original source file
    and running the associated tests.
    """
    
    def __init__(self, base_path: str = None):
        """
        Initialize the validator.
        
        Args:
            base_path: Base path of the project (defaults to current directory)
        """
        self.base_path = base_path or os.getcwd()
    
    def _get_indent(self, line: str) -> str:
        """Extract leading whitespace from a line."""
        return line[:len(line) - len(line.lstrip())]
    
    def _patch_source(self, source_content: str, fix_content: str, config: dict) -> str:
        """
        Patch the fix snippet into the source content.
        
        Args:
            source_content: Original source file content
            fix_content: Fix snippet content (just the method body)
            config: Patch configuration dict
            
        Returns:
            Patched source content
        """
        lines = source_content.split('\n')
        
        # Find the start of the method
        start_idx = None
        end_idx = None
        method_indent = ""
        
        for i, line in enumerate(lines):
            if config["start_marker"] in line:
                start_idx = i
                # Apply offset if specified (e.g., go back from docstring to method def)
                if "start_offset" in config:
                    start_idx += config["start_offset"]
                method_indent = self._get_indent(lines[start_idx])
                break
        
        if start_idx is None:
            raise ValueError(f"Could not find start marker: {config['start_marker']}")
        
        # Find the end of the method (next method at same or lower indent, or end marker)
        for i in range(start_idx + 1, len(lines)):
            if config["end_marker"] in lines[i]:
                end_idx = i
                break
            # Also check for @classmethod or @staticmethod decorators
            if lines[i].strip().startswith('@') and self._get_indent(lines[i]) == method_indent:
                end_idx = i
                break
        
        if end_idx is None:
            # Allow patching until EOF for methods that are the last item in the file.
            end_idx = len(lines)
        
        # Prepare the fix content with proper indentation
        fix_lines = fix_content.strip().split('\n')
        indented_fix_lines = []
        for line in fix_lines:
            if line.strip():  # Non-empty line
                indented_fix_lines.append(method_indent + line)
            else:
                indented_fix_lines.append("")
        
        # Assemble the patched content
        result_lines = lines[:start_idx] + indented_fix_lines + [""] + lines[end_idx:]
        return '\n'.join(result_lines)
    
    def validate(
        self, 
        fix_path: str, 
        test_path: str, 
        defect_id: str,
        timeout: int = 30
    ) -> dict:
        """
        Validate a fix snippet against a test file.
        
        Args:
            fix_path: Path to the fix snippet file (just the method code)
            test_path: Path to the test file
            defect_id: ID of the defect (e.g., "defect1")
            timeout: Max execution time in seconds
            
        Returns:
            Dict containing 'passed' (bool), 'output', and 'error'
        """
        if defect_id not in PATCH_CONFIG:
            return {
                "passed": False,
                "output": "",
                "error": f"Unknown defect ID: {defect_id}"
            }
        
        config = PATCH_CONFIG[defect_id]
        source_path = os.path.join(self.base_path, config["source_path"])
        
        with tempfile.TemporaryDirectory() as sandbox_dir:
            try:
                # 1. Read the original source file
                with open(source_path, 'r') as f:
                    source_content = f.read()
                
                # 2. Read the fix snippet
                with open(fix_path, 'r') as f:
                    fix_content = f.read()
                
                # 3. Patch the source with the fix
                patched_content = self._patch_source(source_content, fix_content, config)
                
                # 4. Write the patched source to sandbox
                dest_source_path = os.path.join(sandbox_dir, f"{config['module_name']}.py")
                with open(dest_source_path, 'w') as f:
                    f.write(patched_content)
                
                # 5. Copy the test file to sandbox
                dest_test_path = os.path.join(sandbox_dir, os.path.basename(test_path))
                shutil.copy(test_path, dest_test_path)
                
                # 6. Execute the test with optional env vars
                env = os.environ.copy()
                if "env_vars" in config:
                    env.update(config["env_vars"])
                
                result = subprocess.run(
                    [sys.executable, os.path.basename(test_path)],
                    cwd=sandbox_dir,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    env=env
                )
                
                return {
                    "passed": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr
                }
                
            except subprocess.TimeoutExpired:
                return {
                    "passed": False,
                    "output": "",
                    "error": f"Execution timed out after {timeout} seconds"
                }
            except Exception as e:
                return {
                    "passed": False,
                    "output": "",
                    "error": f"Validation harness error: {str(e)}"
                }
    
    def validate_all(self, fixes_dir: str, tests_dir: str) -> dict:
        """
        Validate all fixes against their corresponding tests.
        
        Args:
            fixes_dir: Directory containing fix files (defect1_fix_raw.py, etc.)
            tests_dir: Directory containing test files
            
        Returns:
            Dict mapping defect IDs to validation results
        """
        results = {}
        
        fix_test_pairs = [
            ("defect1", "defect1_fix_raw.py", "test_hit01_complete.py"),
            ("defect2", "defect2_fix_raw.py", "test_hit02_complete.py"),
            ("defect3", "defect3_fix_raw.py", "test_hit03_complete.py"),
            ("defect4", "defect4_fix_raw.py", "test_hit04_complete.py"),
            ("defect5", "defect5_fix_raw.py", "test_hit05_complete.py"),
            ("defect6", "defect6_fix_raw.py", "test_hit06_complete.py"),
            ("defect7", "defect7_fix_raw.py", "test_hit07_complete.py"),
            ("defect8", "defect8_fix_raw.py", "test_hit08_complete.py"),
            ("defect9", "defect9_fix_raw.py", "test_hit09_complete.py"),
            ("defect10", "defect10_fix_raw.py", "test_hit10_complete.py"),
            ("defect11", "defect11_fix_raw.py", "test_hit11_complete.py"),
            ("defect12", "defect12_fix_raw.py", "test_hit12_complete.py"),
        ]
        
        for defect_id, fix_file, test_file in fix_test_pairs:
            fix_path = os.path.join(fixes_dir, fix_file)
            test_path = os.path.join(tests_dir, test_file)
            
            if not os.path.exists(fix_path):
                results[defect_id] = {
                    "passed": False,
                    "output": "",
                    "error": f"Fix file not found: {fix_path}"
                }
                continue
            
            if not os.path.exists(test_path):
                results[defect_id] = {
                    "passed": False,
                    "output": "",
                    "error": f"Test file not found: {test_path}"
                }
                continue
            
            results[defect_id] = self.validate(fix_path, test_path, defect_id)
        
        return results


if __name__ == "__main__":
    # Run validation from command line
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate fix snippets by patching")
    parser.add_argument("--base-path", default=os.getcwd(), help="Base project path")
    args = parser.parse_args()
    
    validator = PatchingValidator(args.base_path)
    
    fixes_dir = os.path.join(args.base_path, "failures/python_defects/minimal_fix")
    tests_dir = os.path.join(args.base_path, "failures/python_defects/tests")
    
    results = validator.validate_all(fixes_dir, tests_dir)
    
    print("\n=== Fix Validation Results ===\n")
    for defect_id, result in results.items():
        status = "✅ PASSED" if result["passed"] else "❌ FAILED"
        print(f"{defect_id}: {status}")
        if not result["passed"]:
            print(f"  Error: {result['error'][:200]}...")
            if result["output"]:
                print(f"  Output: {result['output'][:200]}...")
        print()
