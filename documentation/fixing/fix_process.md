# Fix Generation and Validation Process

This document outlines the pipeline for generating, applying, and validating code fixes.

## 1. Fix Generation

The system supports two fix generation modes:

### 1a. Standard Fix Generation (with Explanation)
**Component:** `src/fix.py` -> `FixGenerator.generate`

The system uses a Large Language Model (LLM) to generate repairs for identified defects.
*   **Prompting**: The LLM is provided with the original source code, a natural language explanation of the bug, and the specific function name to target.
*   **Structured Output**: The LLM is forced to return a JSON object conforming to the `FixResponse` Pydantic schema:
    *   `thought_process`: Reasoning behind the fix.
    *   `code`: The raw Python code for the fixed function *only* (not the whole file).

### 1b. Direct Fix Generation (No Explanation - Baseline)
**Component:** `src/fix.py` -> `FixGenerator.generate_direct`

This mode generates fixes directly from source code without an intermediate explanation step, serving as a baseline to measure the value of explanations.
*   **Prompting**: The LLM receives only the source code and target function name (no bug diagnosis).
*   **Use Case**: Comparing fix success rates between explanation-aided and direct fixes.
*   **Activation**:
    *   Canonical: run `./venv/bin/python3 scripts/standalone/run_no_explanation_baseline_run.py`
    *   Legacy: `scripts/run_pipeline.py --no-explanation-baseline`

## 2. Output Validation
**Component:** `src/fix.py` -> `FixGenerator.generate` (internal)

Before applying the fix, the system validates the LLM output:
1.  **Schema Validation**: Pydantic ensures the output structure matches `FixResponse`.
2.  **Candidate Construction**:
    *   The returned function-only snippet is **dedented**.
    *   If `function_name` is provided, the snippet is **spliced into the original module** (see Section 3) to form a full-file candidate.
3.  **Syntax Check**: `ast.parse(candidate)` is called on the full candidate module (or on the snippet if no splicing is needed).
4.  **Fallback**: On `SyntaxError`, the pipeline falls back to the **original source** (while still saving the raw snippet artifact).

## 3. Fix Application
**Component:** `src/fix.py` -> `FixGenerator.apply_fix`

The fix is applied surgically to the original file using Abstract Syntax Tree (AST) analysis:
1.  **Parsing**: The original file is parsed into an AST.
2.  **Targeting**: The system walks the AST to find the specific `FunctionDef` node matching the target function name (supporting both top-level functions and class methods).
3.  **Indentation**: The original indentation level is detected from the source file. The new code is dedented and then re-indented to match the original context.
4.  **Splicing**: The lines corresponding to the old function (including decorators, if present) are replaced with the new, correctly indented lines. The rest of the file remains strictly untouched.

## 4. Validation
**Component:** `src/validation.py` -> `FixValidator.validate`

The generated fix is validated in a clean, isolated environment:
1.  **Isolation**: A temporary directory (`tempfile.TemporaryDirectory`) is created.
2.  **Staging**: 
    *   The fixed file is copied to the temp directory and renamed to the module name expected by the test (e.g., `hit01_timezone.py`).
    *   The corresponding test file is copied to the same directory.
3.  **Execution**: `subprocess.run` executes the test file in this isolated directory. This forces Python to import the local "fixed" module instead of any installed package.
4.  **Result**: The process exit code determines pass (0) or fail (non-zero).

## 5. Assumptions and Limitations
Given the scope of the thesis and the nature of the targeted defects, the following assumptions apply to the validation process:

*   **Limited Fix Complexity**: Since the generated fixes address specific code failures and do not introduce complex new behavior or broad architectural changes, full **regression testing is omitted**. The focus is on validating the resolution of the identified bug.
*   **Test Sufficiency**: The provided test cases are assumed to be a **sufficient specification** of the expected behavior for the component being fixed. A fix is considered "correct" if it satisfies the criteria of the triggering test case.
