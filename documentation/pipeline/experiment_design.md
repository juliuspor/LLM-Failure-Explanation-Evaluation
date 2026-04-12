# Experiment Design (Methodology)

This document defines the **experimental conditions** (context configurations), how they are enumerated, and how the canonical runners execute and resume runs.

---

## Defects Under Test
The experiment operates on `python_defects` in `src/data.py`. Each defect specifies:
- `source_path`: buggy module
- `test_path`: triggering test file
- `function_name`: target function/method (supports `Class.method`)
- `error`: failure message (used as the `[ERROR]` context)
- `ground_truth`: natural-language root-cause description (used for explanation evaluation only)

---

## Context Levels (Atomic Factors)
Context levels are implemented as a bitflag enum: `src/experiment.py` (`ContextLevel`).

The **8 atomic levels** are:
- `CODE`: extracted target function/method body (docstring excluded)
- `ERROR`: defect’s error message
- `TEST`: full triggering test file contents
- `DOCSTRING`: extracted docstring of the target function/method
- `SLICE_BLOCK`: innermost enclosing block around the failure site
- `SLICE_BACKWARD`: dynamic backward slice (execution-trace-based)
- `SLICE_FORWARD`: static forward slice (function-scoped downstream)
- `SLICE_UNION`: union of backward + forward slices

### BASELINE configuration
The special configuration name `BASELINE` refers to the bitwise OR of **all 8 atomic levels**.

**Naming rule:** `src/experiment.py` (`Experiment.levels_to_string`) returns `"BASELINE"` iff all 8 atomic flags are present.

Methodology implication:
- A `BASELINE` explanation prompt includes **all** of: `[CODE]`, `[ERROR]`, `[TEST]`, `[DOCSTRING]`, and all slice sections (`[SLICE_BLOCK]`, `[SLICE_BACKWARD]`, `[SLICE_FORWARD]`, `[SLICE_UNION]`).

---

## Configuration identifiers (how levels are named)
Each configuration is assigned a string `levels_name` via `Experiment.levels_to_string(levels)` and is used in:
- explanation filenames: `defect_id_<levels_name>_run<run_id>.txt`
- fix filenames: `defect_id_<levels_name>_run<run_id>_fix*.py`
- results entries: `results_run<run_id>.json` field `levels`

Naming properties:
- For non-baseline configurations, `levels_name` is the underscore-joined set of included level names in the enum’s fixed order (e.g., `CODE_ERROR_TEST`, `ERROR_SLICE_BACKWARD`).
- For `BASELINE`, the string is literally `BASELINE` (not the long underscore form).

The no-explanation baseline uses a fixed `levels_name`:
- `NO_EXPLANATION` (see `scripts/standalone/run_no_explanation_baseline_run.py`)

---

## Experiment sets (canonical runners)

All canonical runners live in `scripts/standalone/` and write into:
`results/<model_slug>/<run_name>/runs/python/` by default.

### A) Isolated levels (+ BASELINE)
**Runner:** `scripts/standalone/run_isolated_run.py`

Configurations:
- 8 isolated configurations: each atomic level alone
- + `BASELINE` appended last

Total configs: `8 + 1 = 9`

Defaults:
- `--run-id 1`
- `--compare-gt` **off by default** (to avoid updating existing run schemas unless requested)

### B) Two-way combinations (+ BASELINE)
**Runner:** `scripts/standalone/run_twoway_run.py`

Configurations:
- all unordered pairs of the 8 atomic levels: `C(8,2) = 28`
- + `BASELINE` appended last

Total configs: `28 + 1 = 29`

Important detail (slices in combinations):
- Because slice types (`SLICE_BLOCK`, `SLICE_BACKWARD`, `SLICE_FORWARD`, `SLICE_UNION`) are treated like any other atomic factor, two-way experiments include **slice+slice** pairs. The explanation prompt will include **one slice section per slice flag present**.

Defaults:
- `--run-id 1`
- `--compare-gt` **off by default**

### C) Three-way combinations (+ BASELINE)
**Runner:** `scripts/standalone/run_threeway_run.py`

Configurations:
- all unordered triples of the 8 atomic levels: `C(8,3) = 56`
- + `BASELINE` appended last

Total configs: `56 + 1 = 57`

Defaults:
- `--run-id 3` (to avoid modifying existing `run1`/`run2` artifacts in established result directories)
- `--compare-gt` **on by default**

Safety guard:
- If `results_run1.json` or `results_run2.json` already exists, the script refuses to run with `--run-id 1` or `--run-id 2` to prevent accidental modification of earlier runs.

Slice-line metadata note:
- This runner intentionally does **not** persist `slice_lines` in `results_run*.json` entries (to match existing run schemas).

### D) No-explanation baseline (direct fix only)
**Runner:** `scripts/standalone/run_no_explanation_baseline_run.py`

Configurations:
- exactly one configuration: `levels = NO_EXPLANATION`

Total configs: `1`

Defaults:
- `--run-id 1`
- `--compare-gt` **on by default**

Methodology implication:
- No explanation is generated and no explanation scores are computed (`scores: null` in results).

---

## Common runner parameters (CLI)
The standalone runners share the same general CLI pattern:
- `--backend {openai,openrouter}` (default: `openai`)
- `--model <model_name>` (default depends on backend; see runner help)
- `--results-dir <path>`
  - May be the run root (e.g., `.../runs`) or the python dir (e.g., `.../runs/python`).
  - Runners normalize this via `resolve_python_dir(...)` so outputs end in `/python/`.
- `--run-id <int>` or `--run-ids <int...>` (run one or many run IDs)
- `--dry-run` (print planned work and exit without LLM calls)
- `--defects defect1_py,defect2_py,...` (optional subset)
- `--compare-gt` / `--no-compare-gt` (toggle minimal-fix comparison where supported)

---

## Resume and artifact reuse (reproducibility behavior)
All canonical runners implement **resume** behavior to allow interrupted runs to continue safely.

### Results-level resume
For a given `run_id`, if `results_run<run_id>.json` already exists:
- it is loaded as a list of entries
- completed attempts are detected by `(defect_id, levels)` (or by `defect_id` alone for `NO_EXPLANATION`)
- completed attempts are skipped (no re-generation)

### File-level reuse
For each attempt, existing artifacts may be reused:
- Explanation `.txt` is reused if present (otherwise generated and written).
- Fix artifacts (`_fix.py`, `_fix_raw.py`, `_fix_thought.txt`) are reused only if **all** required files exist (otherwise regenerated and written).

### Atomic writes
Runners write `results_run<run_id>.json` via:
- write to `results_run<run_id>.json.tmp`
- `os.replace` to atomically swap into place

This reduces the risk of corrupted results files after interruptions.
