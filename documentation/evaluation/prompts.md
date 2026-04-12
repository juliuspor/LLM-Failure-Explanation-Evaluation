# Prompt Templates (Verbatim)

This document records the **exact prompt templates** used by the pipeline.

Notes:
- Prompts are sent as a single user message (`role="user"`) via `src/llm.py` (`LLMService`).
- The pipeline uses “structured output” schemas, but backend-specific fallback behavior can accept non-JSON outputs (documented in `documentation/evaluation/evaluation_and_llm_methodology.md`).

---

## 1) Explanation generation prompt
**Source:** `src/experiment.py`

### 1.1 Output-format instructions (constant)
```text
[OUTPUT FORMAT]
Return ONLY a valid JSON object with exactly this key:
{"explanation": "..."}

Rules:
- Output exactly one top-level JSON object (no surrounding text).
- Use exactly the key "explanation" (no extra keys).
- The value must be a valid JSON string. If you need newlines, write "\n" inside the string (do not include literal newlines).
- Do not wrap the JSON in Markdown fences.
```

### 1.2 Explanation criteria instructions (constant)
```text
Your explanation should NOT:
- Use jargon or complex language that obscures the issue
- Leave the developer guessing about the root cause
- Omit what happened, why it happened, or where it occurred
- Suggest fixes that are vague or lack a list of steps
- Fail to reference specific variable names, method names, or line numbers from the code
- Include unnecessary filler or redundant information
```

### 1.3 Prompt assembly logic (template)
**Source:** `Experiment.get_prompt(levels)`

The prompt is assembled in this order:
```text
Explain why this code fails.

<OUTPUT_FORMAT_INSTRUCTIONS>

[CODE]
<function code extracted from source_path, docstring excluded>

[ERROR]
<defect["error"]>

[TEST]
<contents of defect["test_path"]>

[DOCSTRING]
<docstring of function_name, if present>

[SLICE_BLOCK]
<slice content>

[SLICE_BACKWARD]
<slice content>

[SLICE_FORWARD]
<slice content>

[SLICE_UNION]
<slice content>

<CRITERIA_INSTRUCTIONS>
```

Important implementation detail:
- Slice sections are included for **every slice flag present** in the `levels` bitmask. In multi-factor runs, this can produce **multiple slice sections** in a single prompt.

---

## 2) Fix generation prompts
**Source:** `src/fix.py`

### 2.1 Explanation-aided fix prompt
**Source:** `FixGenerator._build_function_prompt(source_code, explanation, function_name)`

```text
You are an expert developer. Fix the bug in the function `{function_name}` based on the diagnosis.

[SOURCE CODE]
{source_code}

[BUG DIAGNOSIS]
{explanation}

[OUTPUT FORMAT]
Return a JSON object with exactly these keys:
- thought_process: brief summary of the fix.
- code: the complete, fully valid Python code for the fixed `{function_name}` only (including decorators if any). Do NOT include a docstring. Do NOT include Markdown fences.
```

### 2.2 Direct fix prompt (no-explanation baseline)
**Source:** `FixGenerator._build_direct_prompt(source_code, function_name)`

```text
You are an expert developer. Fix any bugs in the function `{function_name}` in the following source code.
        
[SOURCE CODE]
{source_code}

[OUTPUT FORMAT]
Return a JSON object with exactly these keys:
- thought_process: brief summary of the fix.
- code: the complete, fully valid Python code for the fixed `{function_name}` only (including decorators if any). Do NOT include a docstring. Do NOT include Markdown fences.
```

---

## 3) Explanation scoring (LLM judge) prompt
**Source:** `src/evaluation.py` (`ExplanationEvaluator._evaluate_with_llm`)

```text
Evaluate the following software failure explanation against the ground truth.

Ground Truth: "{ground_truth}"

Explanation: "{explanation}"

[OUTPUT FORMAT]
Return ONLY a valid JSON object with exactly these keys:
{"C2": 0, "C3": 0, "C4": 0, "C6": 0, "reasoning": "..."}

Rules:
- Output exactly one top-level JSON object (no surrounding text).
- Use exactly the keys: C2, C3, C4, C6, reasoning (no extra keys).
- C2/C3/C4/C6 must be integers 0 or 1.
- reasoning must be a JSON string. If you need newlines, write "\n" (do not include literal newlines).
- Do NOT output Markdown, tables, or code fences.

Criteria:
- C2 (Problem Identification): 1 if the explanation correctly identifies the ROOT CAUSE. 
  * STRICT REJECTION: If the explanation only restates the error message (symptom) without explaining WHY it happened, score 0.
- C3 (Explanation Clarity): 1 if the explanation provides a complete CAUSAL CHAIN.
  * STRICT REJECTION: The "Why" must explicitly explain how the code logic led to the failure. If the explanation is circular, gaps exist, or it just says "it failed", score 0.
- C4 (Actionability): 1 if the explanation provides a concrete, numbered list of steps (1., 2., 3.) that explicitly reference specific variable names, function names, or line numbers found in the code.
  * STRICT REJECTION: Score 0 for generic advice like "check the index" or "fix the loop" if the specific variable name (e.g., `i`, `max_val`) is not mentioned in the steps.
- C6 (Brevity): 1 if the explanation is concise and information-dense (little repetition, mostly useful details). 0 if it is overly verbose/rambling OR too sparse to be useful.
- reasoning: Explain why you assigned these scores.
```

