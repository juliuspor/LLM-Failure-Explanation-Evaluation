"""
Smoke test Structured Outputs on a real defect prompt.

Goal: verify that the configured backend/model can produce parseable structured outputs
for the *actual* pipeline prompts (explain → eval → fix) on a single defect/config.

This script does NOT write to `results/`. It can optionally validate the generated fix
in a temporary sandbox directory.

Example (OpenRouter + Grok 4.1 Fast):
  ./venv/bin/python3 scripts/standalone/smoke_structured_outputs_real_defect.py \\
    --backend openrouter --model x-ai/grok-4.1-fast \\
    --defect defect1_py --levels CODE,ERROR,TEST --mode all
"""

from __future__ import annotations

import argparse
import ast
import os
import sys
import tempfile
import textwrap

# Add project root to sys.path before importing from scripts/src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from scripts._common import load_env  # noqa: E402

from src import python_defects  # noqa: E402
from src.evaluation import EvaluationScores  # noqa: E402
from src.experiment import Experiment, ExplanationResponse, parse_levels  # noqa: E402
from src.fix import FixGenerator, FixResponse  # noqa: E402
from src.llm import LLMService  # noqa: E402
from src.validation import FixValidator  # noqa: E402


def _get_defect(defect_id: str) -> dict:
    defect = next((d for d in python_defects if d.get("id") == defect_id), None)
    if defect is None:
        known = [d.get("id") for d in python_defects if d.get("id")]
        raise SystemExit(f"Unknown defect id: {defect_id!r}. Known: {known}")
    return defect


def _build_eval_prompt(*, explanation: str, ground_truth: str) -> str:
    return f"""Evaluate the following software failure explanation against the ground truth.

Ground Truth: "{ground_truth}"

Explanation: "{explanation}"

[OUTPUT FORMAT]
Return ONLY a valid JSON object with exactly these keys:
{{"C2": 0, "C3": 0, "C4": 0, "C6": 0, "reasoning": "..."}}

Rules:
- Output exactly one top-level JSON object (no surrounding text).
- Use exactly the keys: C2, C3, C4, C6, reasoning (no extra keys).
- C2/C3/C4/C6 must be integers 0 or 1.
- reasoning must be a JSON string. If you need newlines, write "\\n" (do not include literal newlines).
- Do NOT output Markdown, tables, or code fences.

Criteria:
- C2 (Problem Identification): 1 if the explanation correctly identifies the ROOT CAUSE.
  * STRICT REJECTION: If the explanation only restates the error message (symptom) without explaining WHY it happened, score 0.
- C3 (Explanation Clarity): 1 if the explanation provides a complete CAUSAL CHAIN.
  * STRICT REJECTION: The "Why" must explicitly explain how the code logic led to the failure. If the explanation is circular, gaps exist, or it just says "it failed", score 0.
- C4 (Actionability): 1 if the explanation provides a concrete, numbered list of steps (1., 2., 3.) that explicitly reference specific variable names, function names, or line numbers found in the code.
  * STRICT REJECTION: Score 0 for generic advice like "check the index" or "fix the loop" if the specific variable name (e.g., `i`, `max_val`) is not mentioned in the steps.
- C6 (Brevity): 1 if the explanation is concise and information-dense (little repetition, mostly useful details). 0 if it is overly verbose/rambling OR too sparse to be useful.
- reasoning: Explain why you assigned these scores."""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Smoke test structured outputs on a real defect prompt (explain → eval → fix)."
    )
    parser.add_argument(
        "--backend",
        choices=["openai", "openrouter"],
        default="openrouter",
        help="LLM backend (default: openrouter).",
    )
    parser.add_argument(
        "--model",
        default=None,
        help=(
            "Model name (default: gpt-5-mini for openai; x-ai/grok-4.1-fast for openrouter). "
            "Example OpenRouter models: x-ai/grok-4.1-fast, deepseek/deepseek-v3.2."
        ),
    )
    parser.add_argument(
        "--defect",
        default="defect1_py",
        help="Defect id from src/data.py (default: defect1_py).",
    )
    parser.add_argument(
        "--levels",
        default="CODE,ERROR,TEST",
        help="Comma-separated context levels for explanation prompt (default: CODE,ERROR,TEST).",
    )
    parser.add_argument(
        "--mode",
        choices=["explain", "eval", "fix", "all"],
        default="all",
        help="Which structured call(s) to test (default: all).",
    )
    parser.add_argument(
        "--response-healing",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Enable OpenRouter response-healing plugin for structured outputs (default: enabled for openrouter).",
    )
    parser.add_argument(
        "--max-total-wait",
        type=int,
        default=60,
        help="Max total retry time in seconds (default: 60).",
    )
    parser.add_argument(
        "--max-wait",
        type=int,
        default=10,
        help="Max wait between retries in seconds (default: 10).",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run fix validation in a temp sandbox (does not affect exit code).",
    )
    parser.add_argument(
        "--validation-timeout",
        type=int,
        default=10,
        help="Validation timeout in seconds (default: 10).",
    )
    parser.add_argument(
        "--print-prompt",
        action="store_true",
        help="Print the explanation prompt verbatim.",
    )
    parser.add_argument(
        "--print-explanation",
        action="store_true",
        help="Print the generated explanation verbatim.",
    )
    parser.add_argument(
        "--print-eval",
        action="store_true",
        help="Print the raw EvaluationScores JSON (model_dump).",
    )
    parser.add_argument(
        "--print-fix",
        action="store_true",
        help="Print the generated fix JSON fields (thought_process + code).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned prompt sizes and exit without LLM calls.",
    )
    args = parser.parse_args()

    if args.model is None:
        args.model = "gpt-5-mini" if args.backend == "openai" else "x-ai/grok-4.1-fast"

    load_env(override=True)

    llm = LLMService(
        backend=args.backend,
        model=args.model,
        max_total_wait=args.max_total_wait,
        max_wait=args.max_wait,
        openrouter_response_healing=args.response_healing if args.backend == "openrouter" else None,
    )

    defect = _get_defect(args.defect)
    exp = Experiment(defect)
    levels = parse_levels(args.levels)
    levels_name = Experiment.levels_to_string(levels)

    explain_prompt = exp.get_prompt(levels)

    print("backend:", args.backend)
    print("model:", args.model)
    print("defect:", defect.get("id"))
    print("levels:", levels_name)
    if args.backend == "openrouter":
        print("response_healing:", llm.openrouter_response_healing)

    if args.print_prompt:
        print("\n=== [explain prompt] ===\n")
        print(explain_prompt)

    if args.dry_run:
        print("\n[dry-run] prompt_chars:", len(explain_prompt))
        return 0

    explanation: str | None = None
    if args.mode in ("explain", "eval", "fix", "all"):
        res = llm.generate_structured(explain_prompt, ExplanationResponse)
        explanation = res.explanation
        if not isinstance(explanation, str) or not explanation.strip():
            raise SystemExit("Structured explanation was empty.")
        print("\n[explain] OK | chars:", len(explanation))
        if args.print_explanation:
            print("\n=== [explanation] ===\n")
            print(explanation)

    if args.mode in ("eval", "all"):
        assert explanation is not None
        ground_truth = defect.get("ground_truth", "")
        eval_prompt = _build_eval_prompt(explanation=explanation, ground_truth=ground_truth)
        scores = llm.generate_structured(eval_prompt, EvaluationScores)
        print("\n[eval] OK |", scores.model_dump())
        if args.print_eval:
            print("\n=== [eval json] ===\n")
            print(scores.model_dump_json(indent=2))

    if args.mode in ("fix", "all"):
        assert explanation is not None
        function_name = defect.get("function_name")
        if not function_name:
            raise SystemExit("Defect is missing function_name; cannot run fix generation.")

        fix_gen = FixGenerator(llm)
        fix_prompt = fix_gen._build_function_prompt(exp.source_code, explanation, function_name)
        fix = llm.generate_structured(fix_prompt, FixResponse)

        snippet = textwrap.dedent(fix.code).strip("\n") + "\n"
        candidate_module = fix_gen.apply_fix(exp.source_code, function_name, snippet)
        ast.parse(candidate_module)

        print("\n[fix] OK | thought_chars:", len(fix.thought_process), "| code_chars:", len(fix.code))
        if args.print_fix:
            print("\n=== [fix json] ===\n")
            print(fix.model_dump_json(indent=2))

        if args.validate:
            module_name = os.path.splitext(os.path.basename(defect["source_path"]))[0]
            validator = FixValidator()
            with tempfile.TemporaryDirectory() as tmp:
                fix_path = os.path.join(tmp, f"{module_name}.py")
                with open(fix_path, "w") as f:
                    f.write(candidate_module)
                validation = validator.validate(
                    fix_path=fix_path,
                    test_path=defect["test_path"],
                    module_name=module_name,
                    timeout=args.validation_timeout,
                )
            print("\n[validate] passed:", bool(validation.get("passed")))
            if validation.get("error"):
                print("[validate] error:", validation.get("error"))

    print("\nAll requested structured calls passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

