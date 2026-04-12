# Evaluation and LLM Methodology

This document specifies (1) how explanation scores C1–C6 are computed and stored, and (2) how the LLM backend layer behaves (structured outputs, retries, and fallbacks).

This is intended to be **thesis-facing methodology**: precise, reproducible, and explicit about failure modes.

---

## 1) Explanation Evaluation (C1–C6)
**Source:** `src/evaluation.py` (`ExplanationEvaluator`)

### 1.1 Inputs
- `explanation`: the model-generated explanation text (from `src/experiment.py`)
- `ground_truth`: the defect’s natural-language root-cause description from `src/data.py`

### 1.2 Outputs (stored)
`ExplanationEvaluator.evaluate(...)` returns a dictionary stored under `scores` in `results_run*.json` with:
- `C1_Readability` (0/1)
- `C2_Problem_Identification` (0/1)
- `C3_Explanation_Clarity` (0/1)
- `C4_Actionability` (0/1)
- `C5_Contextual_Adequacy` (0/1)
- `C6_Brevity` (0/1)
- `reasoning` (string; produced by the LLM judge)

All criteria are **binary in stored results**, even though some are computed from continuous signals.

### 1.3 C1 (Readability): Flesch–Kincaid grade level → binary
**Implementation:** `_calculate_flesch_kincaid(text)`

Procedure:
1. Tokenize words via regex `\\b\\w+\\b`.
2. Split sentences via regex `[.!?]+` and count non-empty segments.
3. Estimate syllables per word using a simple vowel-group heuristic:
   - Count transitions into vowels (`aeiouy`), subtract 1 if word ends with `e`, clamp to at least 1.
4. Compute grade level:
   - `0.39*(words/sentences) + 11.8*(syllables/words) - 15.59`
5. Round to 2 decimals.

Binary conversion:
- `C1_Readability = 1` iff grade level `<= 12.0` (threshold constant `READABILITY_THRESHOLD`)

### 1.4 C5 (Contextual adequacy): code-reference counting → binary
**Implementation:** `_count_code_references(text)`

Two patterns are counted and summed:
- **Line references:** `\\b(line|L)\\s*\\d+` (case-insensitive), e.g., “line 12”, “L12”
- **Method references:** `\\b[a-zA-Z0-9_]+\\(\\)` e.g., `foo()`, `bar_1()`

Binary conversion:
- `C5_Contextual_Adequacy = 1` iff count `>= 2` (threshold constant `CONTEXT_THRESHOLD`)

### 1.5 C2/C3/C4/C6: LLM-judge scoring → binary storage
**Implementation:** `_evaluate_with_llm(explanation, ground_truth)`

The judge is prompted to emit this structured JSON object:
```json
{"C2": 0, "C3": 0, "C4": 0, "C6": 0, "reasoning": "..."}
```

Stored conversions:
- `C2_Problem_Identification = C2` (already binary)
- `C3_Explanation_Clarity = C3` (already binary)
- `C4_Actionability = C4` (already binary)
- `C6_Brevity = C6` (already binary)
- `reasoning = reasoning` (verbatim judge justification)

All four LLM-judged criteria (C2/C3/C4/C6) are requested as binary 0/1 directly from the judge.

### 1.6 Failure handling in evaluation
If the judge call fails (exception), `_evaluate_with_llm` returns:
- `C2=C3=C4=C6=0`
- `reasoning` set to an error message string

This means judge failures deterministically map to an “all-fail” score vector in `scores`.

---

## 2) LLM Backend Methodology
**Source:** `src/llm.py` (`LLMService`)

### 2.1 Backends and models
The LLM layer supports:
- **OpenAI backend** (`backend="openai"`) via `OpenAI()` (requires `OPENAI_API_KEY`)
- **OpenRouter backend** (`backend="openrouter"`) via `OpenAI(base_url="https://openrouter.ai/api/v1")` (requires `OPENROUTER_API_KEY`)

Default model selection is handled by runner scripts (commonly `gpt-5-mini` for OpenAI; commonly `deepseek/deepseek-v3.2` for OpenRouter, but other OpenRouter models such as `x-ai/grok-4.1-fast` are supported).

### 2.2 Determinism controls
All calls use:
- `temperature=0`

Note: despite deterministic decoding settings, **service-level nondeterminism** can still exist (e.g., routing differences, model updates, transient retries).

### 2.3 Retry and backoff (transient failures)
LLM calls are wrapped with `_retry_with_backoff(...)` for transient errors:
- Retried exception types: rate limit, connection errors, timeouts, internal server errors.

Backoff schedule:
- Exponential with jitter: `min(2**attempt, max_wait) + U(0,1)`
- Hard stop: give up when total waited time would exceed `max_total_wait`

This affects run time, and can affect which requests succeed, but does not introduce intentional randomness into prompt content.

### 2.4 Reasoning-effort parameters
Some backends/models support additional reasoning parameters:
- For **OpenAI**: `reasoning_effort` is only attached when the model name starts with `gpt-5` (see `_supports_reasoning_effort()`).
- For **OpenRouter**: reasoning control is expressed via `extra_body.reasoning` (either `effort` or `max_tokens`, not both).

### 2.5 Structured outputs (two enforcement paths)
The pipeline uses structured response models (Pydantic) for:
- explanations (`{"explanation": ...}`)
- fix generation (`{"thought_process": ..., "code": ...}`)
- LLM-judge scoring (`{"C2": ..., "C3": ..., "C4": ..., "C6": ..., "reasoning": ...}`)

#### OpenAI backend (Instructor path)
For `backend="openai"`, `generate_structured(...)` uses `instructor.from_openai(client)` and calls:
- `instructor_client.chat.completions.create(response_model=..., ...)`

If this raises non-transient errors (including parse/validation errors), the exception propagates to the caller, which may:
- fail the attempt (explanation generation) or
- default scores to 0 (evaluation) or
- return empty fix artifacts (fix generation)
depending on the calling module’s error handling.

#### OpenRouter backend (JSON Schema path + fallback)
For `backend="openrouter"`, `generate_structured(...)` uses `response_format={"type":"json_schema", ...}` with `strict=True`.

If the returned message content is not valid JSON (or validation fails), the implementation attempts:
1. Strip Markdown fences if present.
2. Parse as JSON; if that fails, extract substring from the first `{` to the last `}` and parse.
3. If still unsuccessful, apply a **heuristic fallback** based on the expected schema:
   - Explanation: wrap raw text as `{"explanation": "<text>"}`.
   - Judge scores: attempt regex extraction of `C2`, `C3`, `C4` and `C6` from free-form text; default missing fields to 0.
   - Fixes: extract the first ```python code block``` if present; otherwise treat the entire text as code.

Methodology implication:
- On OpenRouter, the “JSON-only” constraint is **best-effort** rather than strictly enforced; some non-JSON outputs can still be accepted and mapped into the schema.

### 2.6 OpenRouter-specific request parameters
When using OpenRouter, the client may send extra parameters via `extra_body`, influenced by:
- `OPENROUTER_SITE_URL` / `OPENROUTER_APP_NAME` (request headers)
- `OPENROUTER_REQUIRE_PARAMETERS` (default: enabled)
- `OPENROUTER_RESPONSE_HEALING` (default: enabled for structured calls; plugin `response-healing`)
- `OPENROUTER_REASONING_EFFORT` or `OPENROUTER_REASONING_MAX_TOKENS`

If both reasoning controls are set, the implementation prefers `reasoning.max_tokens` and omits `reasoning.effort` for determinism.

Model-specific default:
- For `x-ai/grok-4.1-fast`, if no `OPENROUTER_REASONING_*` is configured (and no constructor override is provided), `LLMService` sends `extra_body.reasoning.effort="minimal"` by default.

### 2.7 Deterministic BadRequest fallbacks
Some non-transient request failures are handled by deterministic retries with adjusted parameters:
- **OpenRouter:** if a route rejects `reasoning.effort="none"` with an error message containing “Reasoning is mandatory”, the client drops the configured `reasoning.effort` and retries (and persists the drop for subsequent calls).
- **OpenAI:** if `reasoning_effort="minimal"` is rejected for a given model, the client retries with `reasoning_effort="low"`.

---

## 3) Where prompt templates are defined
Verbatim prompt templates for:
- explanation generation,
- fix generation, and
- judge-based scoring
are recorded in `documentation/evaluation/prompts.md`.

---

## 4) Cross-run explanation metrics analysis (consistency and score→pass-rate)
**Sources:** `scripts/explanation_metrics.py`, `scripts/standalone/analyze_explanation_metrics.py`

### 4.1 When it runs
The report generator (`scripts/generate_report.py`) attempts to run explanation-metrics analysis when:
- the loaded dataset contains at least **two distinct `run_id` values**, and
- at least one entry has `scores != null` (i.e., explanations were generated).

If conditions are met, it writes JSON outputs into the run’s `reports/` directory:
- `explanation_metrics_consistency.json`
- `explanation_metrics_correlation.json`

### 4.2 Consistency analysis (repeatability across runs)
For each `(defect_id, levels)` configuration with at least two runs available:
1. Collect the per-run `scores` dictionaries.
2. For each criterion in `{C1..C6}`, count whether **all runs** assign the exact same value as the first run.
3. Also count an “all criteria match” indicator when the entire score vector matches across runs.

The analysis reports:
- overall per-criterion match rates across all comparable configurations
- per-level match rates (grouped by `levels`)

### 4.3 Score→pass-rate analysis (association, not a correlation coefficient)
This analysis relates explanation scores to fix-validation success using `validation.passed` (or legacy `verification.passed` if present).

Key computations:
- **Total explanation score per attempt:** sum of numeric values in `{C1..C6}` for that attempt.
- **Per-level summaries:** average criterion values and average total score by `levels`, plus that level’s fix pass rate.
- **Quartile analysis:** all attempts are sorted by total score and split into quartiles (Q1–Q4) using `n//4` sizing; pass rate is computed per quartile.
- **Per-criterion deltas:** for each criterion, compute pass rate when the criterion is 1 vs when it is 0; report the difference.

Limitations (methodology):
- This is a discrete-score association analysis; it does **not** compute formal statistical correlations.
- Missing validation entries default to `passed=False` in the analysis code path.
