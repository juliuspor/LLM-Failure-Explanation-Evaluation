# Ground Truth Comparison Process

This document outlines the pipeline for comparing LLM-generated fixes against minimal "ground truth" fixes to evaluate repair efficiency and quality.

## 1. Ground Truth Definition
**Location:** `failures/python_defects/minimal_fix/`

For each defect, a ground truth file is maintained (e.g., `defect1_fix_raw.py`). These files contain the **minimal "raw" function/method** required to resolve the defect, isolating the logical fix from surrounding file boilerplate.

## 2. Robust Normalization
**Component:** `src/utils.py` -> `normalize_python_code`

To ensure comparison is based on logical equivalence rather than formatting, both the ground truth and the LLM-generated fix are normalized:
1.  **AST Parsing**: The code is parsed into an Abstract Syntax Tree.
2.  **Element Removal**: Docstrings and comments are recursively stripped from the tree.
3.  **Alpha-Renaming**: Local variable names are renamed to canonical identifiers (`v0`, `v1`, ...) based on order of definition. Only variables defined within the function scope (assignments, parameters, exception handlers) are renamed; external references (class attributes, module functions, built-ins) are preserved.
4.  **Canonicalization**: The tree is unparsed back into a string with standard formatting, ensuring a "logic-only" representation.

## 3. Comparison Logic
**Component:** `scripts/generate_report.py` -> `compare_with_ground_truth`

The comparison is triggered automatically by the reporting script (can be disabled with `--no-compare-gt`). **Note:** Comparison is performed for **all** fix attempts (both passed and failed), enabling analysis of expected vs actual changed lines across all runs.

1.  **Normalization**: Both the `_fix_raw.py` (generated) and the ground truth are normalized.
2.  **Strict Match**: `is_minimal_fix` is set to `True` if the normalized strings match perfectly.
3.  **Diff Generation**: A unified diff is generated using Python's `difflib` from the normalized versions.
4.  **Changed Lines Analysis**: Both expected (from GT) and actual (from generated fix) changed lines are identified.
5.  **Slice Coverage**: If slice information is available, coverage metrics are computed.

## 4. Evaluation Metrics
The comparison enriches the evaluation results with quantitative data.

> [!IMPORTANT]
> **Metric aggregation differs by pass status:**
> - **Minimal Fix Rate, Line Deviation, Jaccard Similarity, Normalized Levenshtein**: Only aggregated into report averages for **passing** fixes (fixes that fail validation are excluded from these averages).
> - **Expected/Actual Changed Lines, Slice Coverage**: Tracked for **all** fix attempts (both passed and failed), enabling diagnosis of why failed fixes went wrong.

| Metric | Description | Aggregated For |
|--------|-------------|----------------|
| **Pass Rate** | The percentage of fix attempts that passed validation (tests + syntax). Calculated as `Passed / Total` for each context level. | All fixes |
| **Minimal Fix Rate** | The percentage of successful fixes that are logically identical to the ground truth. | Passing fixes only |
| **Line Deviation** | The total number of added and removed lines in the **normalized** diff. This measures "chattiness" or over-engineering in the generated fix. | Passing fixes only |
| **Jaccard Similarity** | Set-based similarity (0.0 to 1.0) between the normalized ground truth and generated fix. Each unique non-empty line is treated as a set element: `Jaccard = |A ∩ B| / |A ∪ B|`. A score of 1.0 indicates identical fixes. | Passing fixes only |
| **Normalized Levenshtein** | Sequence-based distance (0.0 to 1.0) between the normalized ground truth and generated fix. Each non-empty line is treated as a sequence element: `Distance = 1.0 - SequenceMatcher.ratio()`. A score of 0.0 indicates identical fixes. Complements Jaccard by being order-sensitive. | Passing fixes only |
| **Expected Changed Lines** | The source-file line numbers that differ between the buggy function and the ground truth fix. These are the lines that *should* be modified to fix the defect. | All fixes |
| **Actual Changed Lines** | The source-file line numbers that differ between the buggy function and the LLM-generated fix. These are the lines that the LLM *actually* modified. | All fixes |

## 5. Slice Coverage Analysis
**Component:** `scripts/generate_report.py` -> `get_expected_changed_lines`, `get_actual_changed_lines`, `compute_slice_coverage`

Slice coverage measures what percentage of the lines requiring changes are included in each slicing strategy. This evaluates whether the slice successfully identifies the relevant buggy code region.

### How It Works
1. **Extract Buggy Function**: The function is extracted from the source file using AST, excluding docstrings.
2. **Diff Against GT Fix**: The extracted function is compared with the ground truth fix using `SequenceMatcher` to get expected changed lines.
3. **Diff Against Generated Fix**: The extracted function is compared with the LLM-generated fix using `SequenceMatcher` to get actual changed lines.
4. **Filter Non-Code Lines**: Comments and blank lines are excluded from the diff results.
5. **Compute Coverage**: For each slice strategy, coverage is calculated for both expected and actual lines:
   ```
   Expected Coverage = |Expected Changed Lines ∩ Slice Lines| / |Expected Changed Lines|
   Actual Coverage = |Actual Changed Lines ∩ Slice Lines| / |Actual Changed Lines|
   ```

### Coverage Metrics
| Metric | Description |
|--------|-------------|
| **Block Expected Coverage** | Percentage of expected fix lines included in the enclosing block slice. |
| **Block Actual Coverage** | Percentage of lines the LLM actually changed that are in the block slice. |
| **Backward Expected Coverage** | Percentage of expected fix lines included in the backward (data dependency) slice. |
| **Backward Actual Coverage** | Percentage of lines the LLM actually changed that are in the backward slice. |
| **Forward Expected Coverage** | Percentage of expected fix lines included in the forward (impact) slice. |
| **Forward Actual Coverage** | Percentage of lines the LLM actually changed that are in the forward slice. |
| **Union Expected Coverage** | Percentage of expected fix lines included in the combined backward + forward slice. |
| **Union Actual Coverage** | Percentage of lines the LLM actually changed that are in the union slice. |

### Interpreting Coverage Metrics
- **High Expected Coverage**: The slice successfully identifies the code region that needs to be fixed.
- **High Actual Coverage**: The LLM's changes stayed within the slice boundaries (focused repair).
- **Low Actual Coverage**: The LLM made changes outside the slice (potentially over-engineering or making unnecessary modifications).

## 6. Reporting
The metrics are automatically integrated into the reporting outputs:
*   **JSON Results**: `results_run[N].json` is updated with a `comparison` object containing:
    - `is_minimal_fix`: Boolean indicating exact match with GT
    - `diff_to_ground_truth`: Unified diff string
    - `line_deviation`: Count of differing lines
    - `jaccard_similarity`: Similarity score (0.0 to 1.0)
    - `normalized_levenshtein`: Distance score (0.0 to 1.0)
    - `expected_changed_lines`: List of source line numbers that should change
    - `actual_changed_lines`: List of source line numbers that the LLM changed
    - `slice_coverage`: Per-strategy coverage metrics (if slices used)
*   **CSV Summary**: `fix_results.csv` includes aggregated metrics:
    - Pass rate, minimal fix rate, average line deviation, average Jaccard similarity, average normalized Levenshtein distance
    - Average expected and actual changed line counts
    - Expected and actual coverage percentages per slice strategy (Block, Backward, Forward, Union)
*   **Visualizations**: `fix_success_rates.png` provides a dual-axis chart comparing pass rates with average line deviation across context levels.
