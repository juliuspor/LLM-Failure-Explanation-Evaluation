"""
Smoke test for Structured Outputs with the configured LLM backend/model.

This script performs minimal structured calls for the three schemas used in the pipeline:
  1) Explanation generation (ExplanationResponse)
  2) Explanation evaluation (EvaluationScores)
  3) Fix generation (FixResponse)

It is intended as a quick sanity check that responses can be parsed/validated and
that fix code is syntactically valid Python.
"""

from __future__ import annotations

import argparse
import ast
import os
import sys

# Add project root to sys.path before importing from scripts/src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from scripts._common import load_env

from src.evaluation import EvaluationScores
from src.experiment import ExplanationResponse
from src.fix import FixResponse
from src.llm import LLMService

load_env(override=True)


def smoke_explain(llm: LLMService) -> None:
    prompt = """Explain why this code fails.

[CODE]
def f():
    return 1 / 0

[ERROR]
ZeroDivisionError: division by zero
"""
    res = llm.generate_structured(prompt, ExplanationResponse)
    if not res.explanation.strip():
        raise SystemExit("ExplanationResponse.explanation is empty")
    print("\n[explain] OK")


def smoke_eval(llm: LLMService) -> None:
    prompt = """Evaluate the explanation against the ground truth.

Ground Truth: "The function divides by zero unconditionally."
Explanation: "It fails because it executes 1/0, which raises ZeroDivisionError."

Return the scores and reasoning.
"""
    res = llm.generate_structured(prompt, EvaluationScores)
    _ = res.model_dump()
    print("\n[eval] OK")


def smoke_fix(llm: LLMService) -> None:
    prompt = """You are an expert software developer tasked with fixing a bug in a specific function.

[SOURCE CODE]
def div(a, b):
    return a / b

[OUTPUT FORMAT]
Return a JSON object with exactly these keys:
- thought_process: brief reasoning about what needs to be fixed
- code: the complete, fully valid Python code for the fixed function/method only (including decorators if any)

[TASK]
1. Rewrite the function `div` so it handles b == 0 by returning 0.
2. In `code`, output ONLY the code for this function. Do not output the entire file.
3. Do NOT include any comments or Markdown fences in `code`.
"""
    res = llm.generate_structured(prompt, FixResponse)
    ast.parse(res.code)
    print("\n[fix] OK")


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke test structured outputs for the configured LLM backend/model.")
    parser.add_argument(
        "--backend",
        choices=["openai", "openrouter"],
        default="openrouter",
        help="LLM backend (default: openrouter).",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model name (default: gpt-5-mini for openai, deepseek/deepseek-v3.2 for openrouter).",
    )
    parser.add_argument(
        "--response-healing",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Enable OpenRouter response-healing plugin for structured outputs (default: enabled for openrouter).",
    )
    parser.add_argument(
        "--mode",
        choices=["explain", "eval", "fix", "all"],
        default="all",
        help="Which structured call(s) to test (default: all).",
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
    args = parser.parse_args()

    if args.model is None:
        args.model = "gpt-5-mini" if args.backend == "openai" else "deepseek/deepseek-v3.2"

    llm = LLMService(
        backend=args.backend,
        model=args.model,
        max_total_wait=args.max_total_wait,
        max_wait=args.max_wait,
        openrouter_response_healing=args.response_healing if args.backend == "openrouter" else None,
    )
    print("backend:", args.backend)
    print("model:", args.model)
    if args.backend == "openrouter":
        print("response_healing:", llm.openrouter_response_healing)

    if args.mode in ("explain", "all"):
        smoke_explain(llm)
    if args.mode in ("eval", "all"):
        smoke_eval(llm)
    if args.mode in ("fix", "all"):
        smoke_fix(llm)

    print("\nAll requested smoke tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
