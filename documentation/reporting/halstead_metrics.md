# Halstead Complexity Metrics

## Overview

Halstead complexity metrics are computed for both the buggy failing functions ("before") and the LLM-generated fixes ("after") to provide objective complexity measures alongside fix validation results.

## What is Measured

Two key metrics are reported:

- **Volume**: Represents the size of the implementation (based on number of operators and operands)
- **Effort**: Represents the mental effort required to understand/generate the code (Volume × Difficulty)

## Scope

### Failure Complexity
Computed on the **failing function only** extracted from the buggy source file (`failures/python_defects/hit*.py`).

### Fix Complexity
Computed as **delta complexity**: Fix Volume/Effort − Baseline Volume/Effort

- Positive delta: Fix is more complex than the original
- Negative delta: Fix reduced complexity
- Zero delta: Complexity unchanged

## Implementation Details

### Library
Uses [`radon`](https://radon.readthedocs.io/) (version 6.0.1) for metric computation via `radon.metrics.h_visit()`.

### Preprocessing
Before computing metrics, code is **dedented** to normalize indentation (especially important for class methods extracted from source files).

### Comments and Docstrings

**Halstead metrics automatically exclude comments and docstrings.**

This is inherent to how radon works:
- Comments are not part of the Python AST
- Docstrings are parsed but excluded from operator/operand counts
- Only executable code contributes to Volume and Effort

**Verification Example:**
```python
# Code with extensive comments/docstrings
def complex_func(a, b, c):
    '''Multi-line docstring explaining the function'''
    # This is a comment
    result = 0  # inline comment
    return result
# Volume: 13.93, Effort: 18.58

# Clean code (no comments)
def complex_func(a, b, c):
    result = 0
    return result
# Volume: 13.93, Effort: 18.58
```

Both produce identical metrics because Halstead measures actual code complexity, not documentation.

## CSV Outputs

### `fix_attempts.csv`
Per-attempt granularity (defect × level × run):

| Column | Description |
|--------|-------------|
| `Defect` | Defect identifier (e.g., `defect1_py`) |
| `Level` | Context level configuration |
| `Run` | Run number (1-3) |
| `Passed` | Fix validation result (0/1) |
| `Baseline_Volume/Effort` | Metrics for buggy function |
| `Fix_Volume/Effort` | Metrics for generated fix |
| `Delta_Volume/Effort` | Fix − Baseline |

### `fix_results.csv`
Aggregated by Level (mean ± std):

| Column | Description |
|--------|-------------|
| `Avg_Baseline_Volume` | Mean baseline volume across attempts |
| `Std_Baseline_Volume` | Standard deviation |
| `Avg_Fix_Volume` | Mean fix volume |
| `Std_Fix_Volume` | Standard deviation |
| `Avg_Delta_Volume` | Mean delta |
| `Std_Delta_Volume` | Standard deviation |
| *(same pattern for Effort)* | |

## Usage

Generate reports with:

```bash
./venv/bin/python3 scripts/generate_report.py --save-csv --no-compare-gt --results-dir results/gpt_5_mini/isolated/runs
```

Outputs are written to the run's `reports/` directory (e.g., `results/gpt_5_mini/isolated/reports/`):
- `fix_attempts.csv` - Per-attempt data
- `fix_results.csv` - Aggregated statistics

## Interpreting Results

### Empty Values (NaN)

Empty Fix_Volume/Effort/Delta values indicate the LLM-generated fix **could not be parsed**:

- **Syntax errors** (e.g., indentation mismatches like `@classmethod` vs `    def`)
- **Invalid Python** that fails AST parsing
- **Missing fix files** (LLM didn't generate output)

**Example:** `defect1_py,DOCSTRING,1,0,185.47,1609.58,,,,`
- `Passed: 0` (failed)
- Empty fix metrics = syntax error prevented parsing

### Passed=0 With Values

Fix **parsed successfully** but **failed tests** (logical error):

**Example:** `defect1_py,TEST,1,0,185.47,1609.58,254.79,1732.57,69.32,122.99`
- Code is syntactically valid
- Fix is ~37% more complex than baseline (Volume 185→255)
- But logic is wrong → tests failed

### Delta = 0.0

**Ideal outcome!** Bug fixed with **no complexity increase**:

**Example:** `defect4_py,SLICE_BLOCK,1,1,504.64,3041.87,504.64,3041.87,0.0,0.0`
- `Passed: 1` (success)
- Identical Halstead scores = same operators/operands
- Clean fix without added complexity

## Notes

- Metrics are computed **on-the-fly** during report generation
- No Halstead data is persisted to `results_run*.json` files
- Missing or unparseable fix files result in `NaN` values
- Baseline metrics are cached to avoid redundant computation

## References

- [Halstead Complexity Metrics - Wikipedia](https://en.wikipedia.org/wiki/Halstead_complexity_measures)
- [Radon Documentation](https://radon.readthedocs.io/en/latest/)
