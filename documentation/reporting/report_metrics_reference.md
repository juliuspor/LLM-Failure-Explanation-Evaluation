# Report Metrics Reference

This document defines **how each reported datapoint is calculated** in this repository, focusing on the artifacts produced by `scripts/generate_report.py` from existing `results_run*.json` files.

It is calculation- and implementation-oriented (what is computed, how it is aggregated, and which attempts are included), not a discussion of results quality.

## Inputs and primary artifacts

### Input: per-attempt results (`results_run*.json`)
The canonical pipeline writes per-attempt entries to `results/<model>/<run_name>/runs/python/results_run*.json`.

Each **attempt** is one JSON object (typically one `defect_id × levels × run_id`) and commonly contains:
- `defect_id` (string)
- `levels` (string; the “Level”/configuration label)
- `run_id` (int)
- `scores` (dict or `null`) with C1–C6 explanation scores
- `validation` (dict) with `passed` (bool) and test outputs (legacy name: `verification`)
- `fix_file` (string; basename of the generated patched module, used to locate `*_raw.py`)
- `comparison` (dict; optional) produced by ground-truth fix comparison logic
- `slice_lines` (dict; optional) mapping slice strategy → list of source-file line numbers

### Output directory
`scripts/generate_report.py` writes reports next to the provided runs directory:
- input: `.../runs/python/`
- output: `.../reports/`

## Report outputs (what `generate_report.py` produces)

### Fix-validation and fix-quality reports
- `reports/fix_results.csv`: **per-level aggregates** (this doc’s primary focus).
- `reports/fix_attempts.csv`: **per-attempt Halstead metrics** (baseline/fix/delta), plus `Passed`.

### Explanation-evaluation reports
- `reports/comparison.csv`: per-level **mean/std** for each criterion C1–C6.
- `reports/defect_breakdown.csv`: per-defect, per-level **mean score** for each criterion C1–C6.

### Cross-run explanation-metrics analysis (JSON)
When multiple runs exist, `generate_report.py` also triggers the standalone analysis in `scripts/standalone/analyze_explanation_metrics.py` via `scripts/explanation_metrics.py`:
- `reports/explanation_metrics_consistency.json`
- `reports/explanation_metrics_correlation.json`

## Shared definitions and conventions

### Attempt inclusion
Unless noted otherwise, aggregation is done over the set of JSON entries loaded from `results_run*.json`.

### “Passed” definition
An attempt is considered **passed** when:
- `entry["validation"]["passed"] == True`
- or (legacy fallback) `entry["verification"]["passed"] == True`

### Grouping key (“Level”)
All per-level aggregation is grouped by:
- `level = entry.get("levels", "unknown")`

### Rounding
As implemented in `scripts/generate_report.py`:
- `Pass_Rate`, `Minimal_Fix_Rate`: rounded to **3 decimals**
- `Avg_Line_Deviation`: rounded to **2 decimals**
- `Avg_Jaccard_Similarity`: rounded to **3 decimals**
- `Avg_Normalized_Levenshtein`: rounded to **3 decimals**
- `Avg_*_Changed_Lines`: rounded to **2 decimals**
- Halstead `Avg_*`/`Std_*`: rounded to **2 decimals**
- Slice-coverage averages: rounded to **3 decimals**

## Fix results (`fix_results.csv`)

**Producer:** `scripts/generate_report.py` (`aggregate_fix_results` → `save_fix_csv`)

### Pass/fail counts and rate
| Column | Calculation | Inclusion / notes |
|---|---|---|
| `Level` | Group key `entry["levels"]` | Missing levels default to `"unknown"`. |
| `Total` | Count of entries with a truthy `validation`/`verification` dict | Entries without validation info are excluded from pass/fail counting. |
| `Passed` | Count of entries where `passed == True` | `passed` comes from `validation.passed` (legacy: `verification.passed`). |
| `Failed` | `Total - Passed` | Counted when validation exists and `passed == False`. |
| `Pass_Rate` | `round(Passed / Total, 3)` | If `Total == 0`, stored as `0.0`. |

### Ground-truth minimality and similarity (aggregated over **passing fixes only**)
These metrics require a `comparison` object with the relevant fields. They are recorded only when the attempt passed validation.

| Column | Calculation | Inclusion / notes |
|---|---|---|
| `Minimal_Fix_Rate` | `round(minimal / Passed, 3)` | `minimal` increments when `passed=True` and `comparison.is_minimal_fix=True`. If `Passed == 0`, stored as `0.0`. |
| `Avg_Line_Deviation` | `round(mean(deviations), 2)` | `deviations` are collected from `comparison.line_deviation` for passing attempts only. If no deviations collected, stored as `0.0`. |
| `Avg_Jaccard_Similarity` | `round(mean(jaccards), 3)` | `jaccards` are collected from `comparison.jaccard_similarity` for passing attempts only. If no jaccards collected, stored as `0.0`. |
| `Avg_Normalized_Levenshtein` | `round(mean(levenshtein_dists), 3)` | `levenshtein_dists` are collected from `comparison.normalized_levenshtein` for passing attempts only. If no values collected, stored as `0.0`. |

**How `comparison.is_minimal_fix` is computed** (`scripts/generate_report.py:compare_with_ground_truth`)
- Read the ground-truth fix `failures/python_defects/minimal_fix/<defect>_fix_raw.py`.
- Read the generated fix function snippet `<fix_file> → <fix_file without .py>_raw.py`.
- Normalize both strings using `src/utils.py:normalize_python_code` (AST-based canonicalization + local-variable alpha-renaming).
- `is_minimal_fix = (gt_norm == raw_norm)`.

**How `comparison.line_deviation` is computed**
- Compute a unified diff between `gt_norm.splitlines()` and `raw_norm.splitlines()`.
- Count the number of diff lines starting with `+` or `-`, excluding the diff header lines `+++` / `---`.
- This yields the **added + removed line count** on normalized code.

**How `comparison.jaccard_similarity` is computed**
- Treat each unique non-empty stripped line as a set element.
- `Jaccard = |A ∩ B| / |A ∪ B|` where A and B are the sets of normalized lines for GT and generated fix.
- Empty-vs-empty is defined as `1.0`.

**How `comparison.normalized_levenshtein` is computed**
- Treat each non-empty stripped line as a sequence element (same granularity as Jaccard, but order-sensitive).
- `Levenshtein = 1.0 - SequenceMatcher(A, B).ratio()` where A and B are the line sequences.
- Result: `0.0` = identical, `1.0` = completely different.
- Empty-vs-empty is defined as `0.0`.

### Expected vs. actual changed lines (diagnostic; aggregated over attempts where data exists)
These metrics use **source-file absolute line numbers** and are populated from the `comparison` object.

| Column | Calculation | Inclusion / notes |
|---|---|---|
| `Avg_Expected_Changed_Lines` | `round(mean(expected_counts), 2)` | `expected_counts` collects `len(comparison.expected_changed_lines)` **only when the list is non-empty**. If no counts collected, the column may be omitted (or appear as blank/NaN). |
| `Avg_Actual_Changed_Lines` | `round(mean(actual_counts), 2)` | `actual_counts` collects `len(comparison.actual_changed_lines)` **only when the list is non-empty**. If no counts collected, the column may be omitted (or appear as blank/NaN). |

**How `comparison.expected_changed_lines` is computed** (`get_expected_changed_lines`)
- Locate the buggy function in the defect’s source file via AST (supports `Class.method`), and extract it while preserving a mapping of `(source_line_number, code_line)`; docstrings are excluded.
- Load the minimal ground-truth fix `*_fix_raw.py`.
- Dedent both buggy and GT lines by removing their respective minimum indentation.
- Use `difflib.SequenceMatcher(...).get_opcodes()` between the buggy lines and GT lines:
  - `replace`/`delete`: mark the corresponding buggy-source lines as “expected to change”.
  - `insert`: mark the **insertion point** (the previous buggy line if possible, otherwise the first buggy line).
- Filter out blank lines and comment-only lines (via `_is_code_line`).
- Result: a set of **source-file absolute** line numbers.

**How `comparison.actual_changed_lines` is computed** (`get_actual_changed_lines`)
Same algorithm as above, but compares buggy function lines against the generated `*_raw.py` fix snippet instead of GT.

### Halstead complexity metrics (volume/effort; aggregated over attempts where values exist)
**Producer:** `scripts/generate_report.py` (`compute_baseline_metrics`, `compute_fix_metrics_for_results`, then aggregated in `aggregate_fix_results`)

Per attempt, metrics are computed using `radon.metrics.h_visit()`:
- **Baseline** metrics are computed from the extracted buggy function (decorators included; docstring excluded), dedented.
- **Fix** metrics are computed from the generated `*_raw.py` snippet, dedented.
- **Delta** metrics are computed as `Fix − Baseline` when both sides exist.

In `fix_results.csv`, each Halstead column is aggregated per level as mean/std over the set of attempts where that value is present:
| Column pattern | Calculation | Inclusion / notes |
|---|---|---|
| `Avg_*` | `round(mean(values), 2)` | `values` includes only non-`None` per-attempt values for that metric. |
| `Std_*` | `round(stdev(values), 2)` | If only one value exists, std is `0.0`. If no values exist, the column may be omitted (or appear blank/NaN). |

Where `*` is one of:
- `Baseline_Volume`, `Baseline_Effort`
- `Fix_Volume`, `Fix_Effort`
- `Delta_Volume`, `Delta_Effort`

### Slice coverage metrics (expected vs. actual; aggregated over attempts where coverage exists)
Slice coverage is computed when both are available:
- `comparison.expected_changed_lines` / `comparison.actual_changed_lines`
- `entry.slice_lines` (line numbers from slicing during pipeline runs)

Per attempt and per slice strategy, coverage is computed in `compute_slice_coverage`:
- `expected_coverage = |expected_lines ∩ slice_lines| / |expected_lines|` (or `1.0` if `expected_lines` is empty)
- `actual_coverage = |actual_lines ∩ slice_lines| / |actual_lines|` (or `1.0` if `actual_lines` is empty)

`fix_results.csv` reports per-level means (rounded to 3 decimals) for these columns when present:
- `Block_Expected_Coverage`, `Block_Actual_Coverage`
- `Backward_Expected_Coverage`, `Backward_Actual_Coverage`
- `Forward_Expected_Coverage`, `Forward_Actual_Coverage`
- `Union_Expected_Coverage`, `Union_Actual_Coverage`

## Fix attempts (`fix_attempts.csv`)
**Producer:** `scripts/generate_report.py` (`save_fix_attempts_csv`)

One row per attempt (defect × level × run):
- `Passed` is `1` iff `validation.passed` (legacy: `verification.passed`)
- `Baseline_*`, `Fix_*`, `Delta_*` are the per-attempt Halstead values described above (may be empty when parsing fails or fix file is missing).

## Explanation evaluation aggregates (`comparison.csv`, `defect_breakdown.csv`)

### Explanation scores (C1–C6) stored in `results_run*.json`
Explanation scoring is produced during pipeline runs (not by `generate_report.py`) and stored as binary values under `entry["scores"]`.

At report time, entries with `scores == null` are skipped for score aggregation.

For exact criterion definitions, see `documentation/evaluation/evaluation_and_llm_methodology.md`. In brief:
- `C1_Readability`: Flesch–Kincaid grade level thresholded to 0/1.
- `C5_Contextual_Adequacy`: threshold on number of code references.
- `C2/C3/C4/C6`: LLM-judge outputs (with C6 thresholded before storage).

### `comparison.csv` (per-level mean/std by criterion)
**Producer:** `scripts/generate_report.py` (`aggregate_scores` → `save_csv`)

For each level and each criterion:
- `Mean = round(mean(binary_scores), 3)`
- `Std = round(stdev(binary_scores), 3)` (or `0.0` if only one value)

### `defect_breakdown.csv` (per-defect mean by criterion)
**Producer:** `scripts/generate_report.py` (`aggregate_by_defect` → `save_defect_csv`)

For each defect and level and each criterion:
- value = `round(mean(binary_scores_across_runs), 3)`
- if no values exist for that defect/level/criterion, stored as `0`

## Cross-run explanation-metrics outputs (`explanation_metrics_*.json`)

### `explanation_metrics_consistency.json`
**Producer:** `scripts/standalone/analyze_explanation_metrics.py:evaluate_consistency`

Unit of analysis: unique `(defect_id, levels)` configurations with scores present in at least two runs.

For each criterion (and for the full score vector):
- A configuration is a “match” when all available runs for that configuration assign the same value as the first run.
- The reported rate is `matches / total_configs`.

Outputs include overall rates and per-level rates.

### `explanation_metrics_correlation.json` (association analysis)
**Producer:** `scripts/standalone/analyze_explanation_metrics.py:analyze_score_passrate_correlation`

Per attempt:
- total explanation score = `sum(C1..C6)` (using the numeric values present in `scores`)
- pass label = `validation.passed` (legacy: `verification.passed`)

Reported analyses:
1. **Level ranking**: per level, average total explanation score and fix pass rate.
2. **Quartiles**: sort attempts by total score and split into Q1..Q4 using `quartile_size = n // 4` (Q4 gets the remainder); compute pass rate per quartile.
3. **Per-criterion deltas**: for each criterion, compute pass rate when criterion=1 vs criterion=0; report the difference.

## RQ4 minimal-fix correlation analysis (`documentation/reporting/rq4_outputs`)

This repo additionally contains a standalone analysis used for the thesis RQ4 write-up (“explanation quality vs. minimal/non-spurious fixes”):

- **Script:** `scripts/standalone/analyze_rq4_minimal_fix_correlation.py`
- **Inputs:** existing `results/<model>/<batch>/runs/python/results_run*.json` and `results/<model>/<batch>/reports/fix_attempts.csv`
- **Outputs (default):** `documentation/reporting/rq4_outputs/`

The script is **read-only** with respect to `results/` (it does not modify `results_run*.json`).

### Quartile definition (consistent with `analyze_explanation_metrics.py`)
For each `(model, batch)`, it:
- collects all attempts with `scores != null`,
- computes `Total_Score = sum(C1..C6)`,
- sorts attempts by `Total_Score`, then splits into Q1..Q4 using `quartile_size = n // 4` (Q4 gets the remainder).

### Outcome aggregation conventions
- Minimality/similarity metrics (minimal fix rate, line deviation, Jaccard, normalized Levenshtein) are summarized **over passing fixes only**.
- Slice coverage metrics are summarized for the subset of attempts where `comparison.slice_coverage` contains the relevant strategy (e.g., `SLICE_UNION`).

### Output files
- `rq4_attempts.csv`: attempt-level table with `Total_Score`, quartile, pass flag, fix-quality metrics, and context-factor indicators.
- `rq4_quartiles_summary.csv`: per `(model, batch, quartile)` aggregates (including minimal-fix rate over passing fixes).
- `rq4_regression_summary.csv`: controlled association estimates for `Total_Score` (cluster-robust by defect).
- `rq4_spearman_correlations.csv`: Spearman correlations between `Total_Score` and fix-quality outcomes (passing fixes).
- `rq4_quartile_deltas_bootstrap_ci.csv`: Q4--Q1 deltas with defect-cluster bootstrap CIs for selected outcomes.
- `rq4_no_explanation_baseline.csv`: no-explanation baseline metrics (conditional on pass; quartiles not defined).
- `rq4_metadata.json`: run metadata (models/batches, counts, bootstrap settings).

## Notes on missing values and column presence
- `fix_results.csv` is built from per-level dictionaries; some columns only appear if any level has that metric populated, and some per-level cells may be blank/NaN when a metric does not apply or has no values.
- `Avg_*_Changed_Lines` are aggregated only when the underlying lists are non-empty (empty lists are treated as “no data” for the average).
- `Avg_Line_Deviation` / `Avg_Jaccard_Similarity` / `Avg_Normalized_Levenshtein` are aggregated over **passing** attempts only.
