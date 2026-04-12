# LLM Failure Explanation Evaluation

Evaluates LLM-generated explanations of software failures using composable context levels.

## Documentation
- `documentation/README.md` — index of methodology + process docs.
- `results/README.md` — orientation for generated outputs and archived legacy runs.

## Structure

```
├── documentation/            # Methodology/process docs and reporting references
│   └── reporting/rq4_outputs/ # RQ4 analysis tables/CSVs kept out of the repo root
├── src/                     # Core modules
│   ├── data.py              # Python defect definitions
│   ├── java_data.py         # Java defect definitions (for contamination control)
│   ├── llm.py               # OpenAI/OpenRouter wrapper with retry
│   ├── experiment.py        # Experiment class with composable ContextLevel
│   ├── slicing.py           # Dynamic program slicing
│   ├── evaluation.py        # C1-C6 metrics (Pydantic/Instructor)
│   ├── fix.py               # Fix Generation (Structured Output)
│   └── validation.py        # Fix Validation (Sandbox Strategy)
├── scripts/
│   ├── _common.py           # Shared bootstrap & CLI helpers
│   ├── standalone/          # Canonical runners (isolated/two-way/three-way/no-explanation)
│   ├── run_pipeline.py      # Legacy pipeline: experiment → eval → fix (writes to results/runs/)
│   ├── run_experiment.py    # Generate explanations
│   ├── run_evaluation.py    # Multi-run evaluation
│   ├── generate_report.py   # Charts and CSVs
│   └── validate_fixes.py      # Batch validate generated fixes
├── failures/
│   ├── python_defects/      # Python defects + tests
│   │   └── minimal_fix/     # Ground-truth minimal fixes (defectN_fix_raw.py)
│   └── java_defects/        # Original Defects4J Java files (for contamination control)
├── user_study/
│   ├── stimuli/             # Fixed explanation texts shown to participants
│   ├── datasets/            # Generated locally; human-subject data is not tracked
│   ├── results/             # Generated locally; participant state JSONs are not tracked
│   └── archive_revised_materials/ # Superseded study materials kept for traceability
└── results/                 # Generated outputs
    ├── <model>/<run_name>/runs/python/ # Per-run artifacts (.txt explanations, _fix.py, _fix_raw.py, _fix_thought.txt, results.json)
    ├── <model>/<run_name>/reports/     # Aggregated charts and CSVs (Explanations + Fix Validation)
    └── archive_legacy/<run_id>/python/ # Legacy results layout (pre `runs/`)
```

This repository currently includes 12 translated Python defects (`defect1_py` … `defect12_py`) registered in `src/data.py`, plus the 12 original Java defects (`defect1_java` … `defect12_java`) from Defects4J registered in `src/java_data.py`.

## Pipeline Flow

The automated pipeline executes the following cycle for each defect and context configuration:

1. **Explanation Generation**: LLM diagnoses the root cause.
2. **Fix Generation**: LLM generates a Python patch.
3. **Evaluation**: System scores the explanation (C1/C5 algorithmic; C2/C3/C4/C6 via LLM judge).
4. **Artifacts**: Saves all results (see below).
5. **Reporting**: Aggregated metrics including explanation criteria AND fix success rates (validation).

### Baseline Mode (No Explanations)

To measure the value of explanations, the pipeline supports a **baseline mode** that skips explanation generation:

```bash
./venv/bin/python3 scripts/standalone/run_no_explanation_baseline_run.py
```

In this mode:
- The LLM receives only the source code (no bug diagnosis explanation)
- Fix is generated directly from source code analysis
- Useful for comparing fix success rates with/without explanations
- The baseline writes to `results/<model>/no_explanation/runs/python/`

### Data-Contamination Control (Java NO_EXPLANATION)

To control for potential data contamination (Defects4J bugs in LLM training data), the pipeline also supports running the NO_EXPLANATION baseline on the **original Java** source files:

```bash
./venv/bin/python3 scripts/standalone/run_java_no_explanation.py
```

In this mode:
- The LLM receives only the original Java source code (no translation, no explanation)
- Fix is generated as Java code (no validation — we cannot compile/run Java tests)
- Results are saved to `results/<model>/no_explanation_java/runs/java/` (raw fix + thought process)
- Compare Java vs. Python NO_EXPLANATION fix quality to assess contamination impact
- Manual correctness analysis stored in `results/<model>/no_explanation_java/java_fix_correctness.csv`

## Quick Start

```bash
# Canonical experiment runners (write to results/<model>/<run_name>/runs/python/)
./venv/bin/python3 scripts/standalone/run_isolated_run.py
./venv/bin/python3 scripts/standalone/run_twoway_run.py
./venv/bin/python3 scripts/standalone/run_threeway_run.py
./venv/bin/python3 scripts/standalone/run_no_explanation_baseline_run.py

# Switch LLM backend/model (example: OpenRouter)
./venv/bin/python3 scripts/standalone/run_isolated_run.py --backend openrouter --model deepseek/deepseek-v3.2
./venv/bin/python3 scripts/standalone/run_isolated_run.py --backend openrouter --model x-ai/grok-4.1-fast

# Fix validation runs during generation; results are stored in results_run*.json ("validation")

# Generate report from existing results
./venv/bin/python3 scripts/generate_report.py --save-plots --save-csv --results-dir results/gpt_5_mini/three_way/runs

# Generate report from legacy results directory
./venv/bin/python3 scripts/generate_report.py --save-plots --save-csv --results-dir results/archive_legacy/29_12/python

# Skip ground truth comparison (avoids updating `results_run*.json`)
./venv/bin/python3 scripts/generate_report.py --save-plots --save-csv --results-dir results/gpt_5_mini/three_way/runs --no-compare-gt
```

**Note**: Default backend/model is OpenAI + `gpt-5-mini` (requires `OPENAI_API_KEY`; writes to `results/gpt_5_mini/...`). OpenRouter requires `OPENROUTER_API_KEY` and writes to `results/<model_slug>/...` (e.g., `results/deepseek_v3_2/...` or `results/grok_4_1_fast/...`). For reproducibility, `LLMService` sets `temperature=0` for both OpenAI and OpenRouter calls (including structured outputs).

## OpenRouter (DeepSeek V3.2)

To run the same pipeline scripts via OpenRouter (DeepSeek V3.2), set:
- `OPENROUTER_API_KEY` (required)
- `OPENROUTER_SITE_URL` (optional)
- `OPENROUTER_APP_NAME` (optional)
- `OPENROUTER_RESPONSE_HEALING` (optional, default: enabled for structured outputs; set to `0` to disable)

Example (isolated levels):

```bash
./venv/bin/python3 scripts/standalone/run_isolated_run.py --backend openrouter --model deepseek/deepseek-v3.2
```

By default, OpenRouter runs write to `results/deepseek_v3_2/...` (separate from `results/gpt_5_mini/...`).

## OpenRouter (xAI Grok 4.1 Fast)

Examples:

```bash
./venv/bin/python3 scripts/standalone/run_isolated_run.py --backend openrouter --model x-ai/grok-4.1-fast --run-ids 1 2 3 --compare-gt
./venv/bin/python3 scripts/standalone/run_twoway_run.py --backend openrouter --model x-ai/grok-4.1-fast --run-ids 1 2 3 --compare-gt
./venv/bin/python3 scripts/standalone/run_threeway_run.py --backend openrouter --model x-ai/grok-4.1-fast --run-ids 1 2 3 --compare-gt
./venv/bin/python3 scripts/standalone/run_no_explanation_baseline_run.py --backend openrouter --model x-ai/grok-4.1-fast --run-ids 1 2 3 --compare-gt
```

By default, this writes to `results/grok_4_1_fast/...` (separate from `results/gpt_5_mini/...`).

Note: For `x-ai/grok-4.1-fast`, `LLMService` enables OpenRouter reasoning with `extra_body.reasoning.effort="minimal"` by default (unless `OPENROUTER_REASONING_*` is explicitly configured).

Structured output smoke test (3 minimal structured calls: explain/eval/fix):

```bash
./venv/bin/python3 scripts/standalone/smoke_structured_outputs.py --backend openrouter --model deepseek/deepseek-v3.2 --mode all
./venv/bin/python3 scripts/standalone/smoke_structured_outputs.py --backend openrouter --model x-ai/grok-4.1-fast --mode all
```

Disable Response Healing (debug structured outputs):

```bash
OPENROUTER_RESPONSE_HEALING=0 ./venv/bin/python3 scripts/standalone/smoke_structured_outputs.py --backend openrouter --model deepseek/deepseek-v3.2 --mode all
```

## Full Experiment Run Commands

### Sequential Runs (all run IDs in one command)

#### OpenAI — GPT-5-mini

| Script | Command |
|--------|---------|
| Isolated | `./venv/bin/python3 scripts/standalone/run_isolated_run.py --backend openai --model "gpt-5-mini" --run-ids 1 2 3 --compare-gt` |
| Two-way | `./venv/bin/python3 scripts/standalone/run_twoway_run.py --backend openai --model "gpt-5-mini" --run-ids 1 2 3 --compare-gt` |
| Three-way | `./venv/bin/python3 scripts/standalone/run_threeway_run.py --backend openai --model "gpt-5-mini" --run-ids 1 2 3 --compare-gt` |
| No-explanation | `./venv/bin/python3 scripts/standalone/run_no_explanation_baseline_run.py --backend openai --model "gpt-5-mini" --run-ids 1 2 3 --compare-gt` |

#### OpenRouter — DeepSeek V3.2

| Script | Command |
|--------|---------|
| Isolated | `./venv/bin/python3 scripts/standalone/run_isolated_run.py --backend openrouter --model "deepseek/deepseek-v3.2" --run-ids 1 2 3 --compare-gt` |
| Two-way | `./venv/bin/python3 scripts/standalone/run_twoway_run.py --backend openrouter --model "deepseek/deepseek-v3.2" --run-ids 1 2 3 --compare-gt` |
| Three-way | `./venv/bin/python3 scripts/standalone/run_threeway_run.py --backend openrouter --model "deepseek/deepseek-v3.2" --run-ids 1 2 3 --compare-gt` |
| No-explanation | `./venv/bin/python3 scripts/standalone/run_no_explanation_baseline_run.py --backend openrouter --model "deepseek/deepseek-v3.2" --run-ids 1 2 3 --compare-gt` |

#### OpenRouter — xAI Grok 4.1 Fast

| Script | Command |
|--------|---------|
| Isolated | `./venv/bin/python3 scripts/standalone/run_isolated_run.py --backend openrouter --model "x-ai/grok-4.1-fast" --run-ids 1 2 3 --compare-gt` |
| Two-way | `./venv/bin/python3 scripts/standalone/run_twoway_run.py --backend openrouter --model "x-ai/grok-4.1-fast" --run-ids 1 2 3 --compare-gt` |
| Three-way | `./venv/bin/python3 scripts/standalone/run_threeway_run.py --backend openrouter --model "x-ai/grok-4.1-fast" --run-ids 1 2 3 --compare-gt` |
| No-explanation | `./venv/bin/python3 scripts/standalone/run_no_explanation_baseline_run.py --backend openrouter --model "x-ai/grok-4.1-fast" --run-ids 1 2 3 --compare-gt` |

### Report Generation (all models × all batches)

```bash
# DeepSeek V3.2
./venv/bin/python3 scripts/generate_report.py --save-plots --save-csv --results-dir results/deepseek_v3_2/isolated/runs
./venv/bin/python3 scripts/generate_report.py --save-plots --save-csv --results-dir results/deepseek_v3_2/no_explanation/runs
./venv/bin/python3 scripts/generate_report.py --save-plots --save-csv --results-dir results/deepseek_v3_2/two_way/runs
./venv/bin/python3 scripts/generate_report.py --save-plots --save-csv --results-dir results/deepseek_v3_2/three_way/runs

# GPT-5-mini
./venv/bin/python3 scripts/generate_report.py --save-plots --save-csv --results-dir results/gpt_5_mini/isolated/runs
./venv/bin/python3 scripts/generate_report.py --save-plots --save-csv --results-dir results/gpt_5_mini/no_explanation/runs
./venv/bin/python3 scripts/generate_report.py --save-plots --save-csv --results-dir results/gpt_5_mini/two_way/runs
./venv/bin/python3 scripts/generate_report.py --save-plots --save-csv --results-dir results/gpt_5_mini/three_way/runs

# Grok 4.1 Fast
./venv/bin/python3 scripts/generate_report.py --save-plots --save-csv --results-dir results/grok_4_1_fast/isolated/runs
./venv/bin/python3 scripts/generate_report.py --save-plots --save-csv --results-dir results/grok_4_1_fast/no_explanation/runs
./venv/bin/python3 scripts/generate_report.py --save-plots --save-csv --results-dir results/grok_4_1_fast/two_way/runs
./venv/bin/python3 scripts/generate_report.py --save-plots --save-csv --results-dir results/grok_4_1_fast/three_way/runs
```

### Java No-Explanation (Contamination Control)

```bash
# OpenAI
./venv/bin/python3 scripts/standalone/run_java_no_explanation.py --backend openai --model gpt-5-mini --run-ids 1 2 3

# DeepSeek
./venv/bin/python3 scripts/standalone/run_java_no_explanation.py --backend openrouter --model deepseek/deepseek-v3.2 --run-ids 1 2 3

# Grok
./venv/bin/python3 scripts/standalone/run_java_no_explanation.py --backend openrouter --model x-ai/grok-4.1-fast --run-ids 1 2 3
```

## Context Levels

Context levels are **isolated and composable** using bitwise OR. Each level provides independent information:

| Level | Description |
|-------|-------------|
| `CODE` | Function body where the failure occurs (excludes docstring) |
| `ERROR` | Error message from test failure |
| `TEST` | Test case that triggers the failure |
| `DOCSTRING` | Docstring of the failing function |
| `SLICE_BLOCK` | Innermost enclosing code block around failure |
| `SLICE_BACKWARD` | Dynamic backward slice (execution history) |
| `SLICE_FORWARD` | Static forward slice (function-scoped) |
| `SLICE_UNION` | Backward + Forward combined |

### Using the Experiment Class

```python
from src import Experiment, ContextLevel, python_defects, LLMService

llm = LLMService()
defect = python_defects[0]
exp = Experiment(defect)

# Single level
exp.run(ContextLevel.ERROR, llm)

# Combined levels
exp.run(ContextLevel.CODE | ContextLevel.ERROR, llm)
exp.run(ContextLevel.TEST | ContextLevel.SLICE_BACKWARD, llm)

# Full context
full = ContextLevel.CODE | ContextLevel.ERROR | ContextLevel.TEST | ContextLevel.SLICE_UNION
exp.run(full, llm)

# Just get the prompt (without running LLM)
prompt = exp.get_prompt(ContextLevel.CODE | ContextLevel.ERROR)
```

## Dynamic Slicing

For Python defects, slices are generated using dynamic program slicing via `src/slicing.py`.

### Slicing Strategies

| Strategy | Description |
|----------|-------------|
| `block` | Innermost enclosing code block around failure |
| `backward` | Dynamic backward slice (execution history) |
| `forward` | Static forward slice (impact analysis, function-scoped) |
| `union` | Backward + Forward combined |

### Standalone Usage

```bash
./venv/bin/python3 src/slicing.py <source_file> <test_file> <strategy>

# Example
./venv/bin/python3 src/slicing.py failures/python_defects/hit01_timezone.py failures/python_defects/tests/test_hit01_complete.py union
```

## Fix Generation & Validation

The pipeline now includes an automated repair stage to assess explanation utility.

### Fix Generation (`src/fix.py`)
*   **Inputs**: Source Code + Generated Explanation + Target Function Name.
*   **Mechanism**: Uses **Structured Outputs** (JSON Schema) to enforce valid Python code generation, validated via `ast.parse`.
*   **Outputs**:
    *   `[id]_[config]_fix.py`: Full patched file ready for execution.
    *   `[id]_[config]_fix_raw.py`: The individual function/method code exactly as returned by the LLM.
    *   `[id]_[config]_fix_thought.txt`: The internal reasoning/thought process for the fix.

### Validation (`src/validation.py`)
*   **Strategy**: **Sandboxed Execution**.
*   **Process**:
    1.  Creates an isolated temporary directory.
    2.  Stages the generated fix (renamed to original module name) and original test file.
    3.  Runs the test suite to validate the repair.
*   **Results**: Stored in `results_run[N].json` with `passed`, `output`, and `error` fields.

### Ground Truth Comparison (enabled by default)
*   **Minimal Fixes**: Compares LLM-generated fixes against a predefined minimal "ground truth" fix.
    *   Ground truth lives in `failures/python_defects/minimal_fix/` as `defectN_fix_raw.py`.
*   **Evaluation Metrics**:
    *   **Pass Rate**: Percentage of fix attempts that passed validation (tests + syntax).
    *   **Minimal Fix Rate**: Percentage of passed fixes that are logically identical to ground truth.
    *   **Line Deviation**: Total added + removed lines compared to ground truth.
    *   **Jaccard Similarity**: Set-based similarity between generated fix and ground truth (0.0 to 1.0).
    *   **Normalized Levenshtein Distance**: Sequence-based distance between generated fix and ground truth (0.0 to 1.0). Complements Jaccard by being order-sensitive.
    *   **Expected Changed Lines**: Source lines that should change to fix the defect (derived from GT comparison).
    *   **Actual Changed Lines**: Source lines that the LLM actually modified in its fix.
*   **Slice Coverage Analysis**: Measures what percentage of lines requiring changes are included in each slicing strategy:
    *   **Expected Coverage**: What % of lines that *should* change are in the slice.
    *   **Actual Coverage**: What % of lines the LLM *actually* changed are in the slice.
*   **Reporting**: Automatically updates `results_run[N].json` with comparison data and populates `fix_results.csv` with:
    *   "Pass Rate", "Minimal Fix Rate", and "Avg Line Deviation"
    *   "Avg Jaccard Similarity"
    *   "Avg Normalized Levenshtein"
    *   "Avg Expected Changed Lines", "Avg Actual Changed Lines"
    *   Expected and Actual slice coverage metrics per strategy (Block, Backward, Forward, Union)

## Evaluation Criteria (LLM + Algorithmic)

Criteria C1-C6 are binary (0/1). For LLM-based criteria, the pipeline now saves the **evaluation reasoning** in the results JSON.

| ID | Criterion | Method | Pass (1) |
|----|-----------|--------|----------|
| C1 | Readability | Algorithm | Flesch-Kincaid ≤ 12 |
| C2 | Problem ID | LLM | Correct Root Cause (vs Symptom) |
| C3 | Clarity | LLM | Complete Causal Chain |
| C4 | Actionability | LLM | Concrete Numbered Steps (1, 2, 3...) |
| C5 | Context | Algorithm | ≥ 2 code refs |
| C6 | Brevity | LLM | Binary: concise & dense = 1 |

## Explanation Metrics Reports (Cross-Run)

When `scripts/generate_report.py` detects **≥ 2 runs** and at least one entry with `scores != null`, it also runs cross-run explanation-metrics analyses and writes JSON outputs to the run’s `reports/` directory:

- `explanation_metrics_consistency.json` — how consistently the LLM assigns C1–C6 scores across runs.
- `explanation_metrics_correlation.json` — pooled association between explanation scores and fix validation pass rates (ranking/quartiles/deltas; not a Pearson/Spearman coefficient).
- `explanation_metrics_within_defect.json` — **within-defect** association (per `defect_id`, across context `levels`) between mean explanation score and outcome rate:
  - functional fix success: `validation.passed`
  - ground-truth minimal-fix match: `comparison.is_minimal_fix` (only when GT comparison data exists; e.g., not available when running `--no-compare-gt`)

Methodology + interpretation: `documentation/evaluation/analyze_explanation_metrics.md`.
