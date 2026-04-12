# Pipeline Overview (Methodology)

This document describes the **end-to-end methodology** used in this repository to (1) generate LLM explanations of software failures under controlled context conditions, and (2) measure whether those explanations help an LLM generate validated fixes.

This is a **process description** (how the pipeline works), not a results discussion.

---

## Scope and Primary Artifacts

### Inputs
- **Defect registry**: `src/data.py` (`python_defects`)
  - Each defect provides: `id`, `source_path`, `test_path`, `function_name`, `error`, and a natural-language `ground_truth` description (used as the explanation-evaluation reference).
- **Source + tests**: `failures/python_defects/*.py` and `failures/python_defects/tests/*.py`
- **(Optional) Minimal-fix ground truth**: `failures/python_defects/minimal_fix/defectN_fix_raw.py` (used to compare generated fixes to a minimal reference fix).

### Outputs
Canonical runners write to:
- `results/<model_slug>/<run_name>/runs/python/` (per-run artifacts)
- `results/<model_slug>/<run_name>/reports/` (aggregated CSV/plots and analysis JSON files)

Per (defect × configuration × run_id), the pipeline typically produces:
- `defectX_py_<LEVELS>_run<run_id>.txt`: explanation text
- `defectX_py_<LEVELS>_run<run_id>_fix.py`: **full patched module** (original file with the function replaced)
- `defectX_py_<LEVELS>_run<run_id>_fix_raw.py`: function-only snippet as returned by the LLM
- `defectX_py_<LEVELS>_run<run_id>_fix_thought.txt`: brief fix rationale (model output field)
- `results_run<run_id>.json`: structured per-attempt records (scores + validation + optional comparison)

---

## Pipeline Stages (per attempt)

### 0) Select context configuration
Each attempt is run under a **ContextLevel configuration** (e.g., `CODE`, `ERROR`, `TEST`, `SLICE_BACKWARD`, or combinations). These configurations are enumerated by the canonical runner scripts under `scripts/standalone/` (see `documentation/pipeline/experiment_design.md`).

### 1) Build an explanation prompt
**Component:** `src/experiment.py` (`Experiment.get_prompt`)

The prompt is assembled from zero or more labeled sections:
- `[CODE]` extracted function/method (docstring excluded)
- `[ERROR]` test failure message from the defect registry
- `[TEST]` full test file contents
- `[DOCSTRING]` docstring of the failing function (if present)
- `[SLICE_*]` one or more slices produced by `src/slicing.py`

The prompt enforces a **JSON-only** output format for the explanation (see `documentation/evaluation/prompts.md` for verbatim templates).

### 2) Generate the explanation (LLM)
**Components:** `src/experiment.py` (`Experiment.run`), `src/llm.py` (`LLMService.generate_structured`)

The explanation is generated via a structured response model:
- Expected JSON schema: `{"explanation": "..."}` (string)

The resulting explanation text is written to `..._run<run_id>.txt`.

**No-explanation baseline:** in the `NO_EXPLANATION` condition, this step is skipped.

### 3) Score the explanation (C1–C6)
**Component:** `src/evaluation.py` (`ExplanationEvaluator.evaluate`)

The pipeline computes **binary** scores for C1–C6:
- C1 and C5 are computed algorithmically.
- C2/C3/C4/C6 are produced by an LLM judge using a structured output schema, then thresholded/converted to binary where needed (notably C6).

The scoring output is stored in `results_run<run_id>.json` under `scores`.

**No-explanation baseline:** in the `NO_EXPLANATION` condition, `scores` is stored as `null`.

### 4) Generate a fix (LLM)
**Component:** `src/fix.py` (`FixGenerator.generate` or `FixGenerator.generate_direct`)

Two fix-generation modes exist:
- **Explanation-aided fix**: input = source code + generated explanation + target `function_name`
- **No-explanation baseline**: input = source code + target `function_name` (no explanation)

Structured output schema:
- `thought_process`: short rationale
- `code`: **function-only** code for the fixed function/method (decorators included if any; no docstring)

Application method:
1. The function-only snippet is dedented.
2. It is **spliced** into the original module using AST location info (only the target function is replaced; rest of file unchanged).
3. The candidate full module is syntax-checked with `ast.parse`; on parse failure the pipeline falls back to the original source.

Artifacts written:
- `..._fix.py` (full module candidate)
- `..._fix_raw.py` (function-only snippet)
- `..._fix_thought.txt` (rationale)

### 5) Validate the fix by running the test in isolation
**Component:** `src/validation.py` (`FixValidator.validate`)

Validation runs the defect’s test file inside a temporary directory:
1. Copy `..._fix.py` into the sandbox and rename it to the expected module name (derived from the original source filename).
2. Copy the test file into the sandbox directory.
3. Execute the test using `sys.executable` with a timeout (default 10s).

The validation result is stored in `results_run<run_id>.json` under `validation`:
- `passed`: boolean (`returncode == 0`)
- `output`: stdout
- `error`: stderr (or harness error/timeout message)

### 6) (Optional) Compare generated fix to a minimal ground-truth fix
**Component:** `scripts/generate_report.py` (`compare_with_ground_truth`), normalization: `src/utils.py` (`normalize_python_code`)

If enabled, the pipeline compares the generated fix’s function-only code to a minimal reference fix:
- Docstrings/comments removed and code normalized via AST.
- Local variables can be alpha-renamed to canonical identifiers for logic-only comparisons.

Comparison outputs can include:
- exact minimality match (normalized string equality)
- line deviation and a normalized unified diff
- Jaccard similarity on normalized lines
- normalized Levenshtein distance on normalized lines
- expected vs actual changed-line sets
- (if slice line data exists) slice-coverage metrics

Details are documented in `documentation/fixing/comparison_process.md`.

### 7) Reporting and aggregation
**Component:** `scripts/generate_report.py`

From one or more `results_run*.json` files, the report generator can produce:
- aggregated CSVs (per-level and per-attempt tables)
- plots comparing levels on explanation scores and fix metrics
- optional Halstead complexity metrics for baseline vs fix (see `documentation/reporting/halstead_metrics.md`)
- optional explanation-metrics analyses across runs (consistency and score→pass-rate analysis; see `documentation/evaluation/evaluation_and_llm_methodology.md`)

---

## Determinism and Reproducibility Notes
- All LLM calls are made with `temperature=0` (deterministic decoding settings), but **model/service nondeterminism can still exist**.
- Canonical runners support **resume** behavior: completed (defect_id, levels) pairs are skipped to allow interrupted runs to continue without overwriting artifacts.
- Result files under `results/` are treated as generated artifacts; the thesis methodology should describe the process independently of any particular run outputs.
