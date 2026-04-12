"""
Validation Module.
Handles the secure execution of generated fixes against test suites.
"""
import subprocess
import tempfile
import shutil
import os
import sys

class FixValidator:
    """
    Validates a fix by running the associated test in an isolated environment.
    """
    
    def validate(self, fix_path: str, test_path: str, module_name: str, timeout: int = 10) -> dict:
        """
        Validate a fix against a test file.
        
        Args:
            fix_path: Path to the generated fix file.
            test_path: Path to the original test file (which imports the module).
            module_name: The name expected by the test import (e.g., 'hit01_timezone').
            timeout: Max execution time in seconds.
            
        Returns:
            Dict containing 'passed' (bool), 'output', and 'error'.
        """
        # Create a temporary directory for isolation
        with tempfile.TemporaryDirectory() as sandbox_dir:
            try:
                # 1. Stage the Fix
                # Copy the generated fix to the sandbox, renaming it to what the test expects
                dest_fix_path = os.path.join(sandbox_dir, f"{module_name}.py")
                shutil.copy(fix_path, dest_fix_path)
                
                # 2. Stage the Test
                dest_test_path = os.path.join(sandbox_dir, os.path.basename(test_path))
                shutil.copy(test_path, dest_test_path)
                
                # 3. Execute
                # Run the test file in the sandbox directory.
                # Python will prefer the local file (our fix) over any installed package.
                result = subprocess.run(
                    [sys.executable, os.path.basename(test_path)],
                    cwd=sandbox_dir,
                    capture_output=True,
                    text=True,
                    timeout=timeout
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
