# Explanation Metrics Analysis

This document describes how to run the **cross-run explanation metrics analysis** on existing `results_run*.json` files.

Methodology details (what is computed and how) are documented in:
- `documentation/evaluation/evaluation_and_llm_methodology.md` (Section “Cross-run explanation metrics analysis”)

## Location
- Standalone script: `scripts/standalone/analyze_explanation_metrics.py`
- Wrapper (used by report generation): `scripts/explanation_metrics.py`

## Usage

### A) Automatic via report generation (recommended)
`scripts/generate_report.py` will attempt to run the analysis automatically when it detects:
- at least **two distinct run IDs**, and
- at least one entry with `scores != null` (i.e., explanations exist).

The outputs are written to the run’s `reports/` directory as:
- `explanation_metrics_consistency.json`
- `explanation_metrics_correlation.json`
- `explanation_metrics_within_defect.json`

Example:
```bash
./venv/bin/python3 scripts/generate_report.py --save-plots --save-csv --results-dir results/<model>/<run_name>/runs
```

### B) Direct standalone invocation (manual/debug)
```bash
./venv/bin/python3 scripts/standalone/analyze_explanation_metrics.py \
  --dir results/gpt_5_mini/two_way/runs/python/ \
  --pattern "results_run*.json" \
  --output consistency_results.json \
  --correlation-output correlation_results.json
```

Both analyses run by default:

### 1. Consistency Analysis
Evaluates how consistently the LLM assigns the same scores across multiple runs.

### 2. Score-to-Pass-Rate Correlation Analysis
Answers: *Does a better-scoring explanation lead to a better fix validation pass rate?*

Note: despite the script name, this is an **association analysis** (ranking + quartiles + deltas), not a Pearson/Spearman correlation coefficient.

**Output includes:**
- Context levels ranked by average explanation score  
- Pass rates by score quartile (Q1-Q4)
- Per-criterion correlation (which criteria best predict fix success)
- Key insights summary

## Arguments

| Argument | Description |
|----------|-------------|
| `--dir` | Directory containing result files |
| `--pattern` | Glob pattern for result files (default: `results_run*.json`) |
| `--output` | Path to save consistency results as JSON |
| `--correlation-output` | Path to save correlation results as JSON |
