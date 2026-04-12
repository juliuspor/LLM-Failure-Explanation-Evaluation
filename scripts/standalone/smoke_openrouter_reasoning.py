"""
Smoke test OpenRouter reasoning controls on a single model.

Goal: quickly verify whether a given OpenRouter model (e.g., deepseek/deepseek-v3.2)
accepts and responds to OpenRouter's unified `reasoning` configuration:

  - reasoning.effort (e.g., none/minimal/low/medium/high/xhigh)
  - reasoning.max_tokens (a direct cap on reasoning tokens, for models that support it)

This script is intentionally independent of the experiment pipeline and `src/llm.py`.
It calls the OpenRouter Chat Completions endpoint via the OpenAI Python SDK and
prints the raw JSON response fields relevant for reasoning tokens.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Literal

from openai import APIError, APIStatusError, OpenAI

# Add project root to sys.path before importing from scripts/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from scripts._common import load_env  # noqa: E402


ReasoningEffort = Literal["xhigh", "high", "medium", "low", "minimal", "none"]


@dataclass(frozen=True)
class Case:
    name: str
    extra_body: dict[str, Any] | None = None
    reasoning_effort: str | None = None  # OpenAI-style top-level param (likely unsupported by OpenRouter models)


def _build_client() -> OpenAI:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY is not set (check your .env or environment).")

    default_headers: dict[str, str] = {}
    site_url = os.environ.get("OPENROUTER_SITE_URL")
    app_name = os.environ.get("OPENROUTER_APP_NAME")
    if site_url:
        default_headers["HTTP-Referer"] = site_url
    if app_name:
        default_headers["X-Title"] = app_name

    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers=default_headers or None,
    )


def _summarize_response(data: dict[str, Any], *, print_content: bool, print_reasoning: bool) -> None:
    usage = data.get("usage")
    choices = data.get("choices") or []
    choice0 = choices[0] if isinstance(choices, list) and choices else {}
    message = choice0.get("message") or {}

    content = message.get("content")
    reasoning = message.get("reasoning") or message.get("reasoning_content")
    reasoning_details = message.get("reasoning_details") or []

    finish_reason = choice0.get("finish_reason")
    print("finish_reason:", finish_reason)

    if usage is not None:
        print("usage:", json.dumps(usage, indent=2, sort_keys=True))

    if isinstance(content, str):
        print("content_chars:", len(content))
        if print_content:
            print("content:", content)
    else:
        print("content:", repr(content))

    if isinstance(reasoning, str):
        print("reasoning_chars:", len(reasoning))
        if print_reasoning:
            print("reasoning:", reasoning)
    else:
        print("reasoning:", repr(reasoning))

    if isinstance(reasoning_details, list):
        types = sorted({d.get("type") for d in reasoning_details if isinstance(d, dict) and d.get("type")})
        print("reasoning_details_items:", len(reasoning_details), "types:", types)
    else:
        print("reasoning_details:", repr(reasoning_details))


def _run_case(
    client: OpenAI,
    *,
    model: str,
    prompt: str,
    max_tokens: int,
    temperature: float,
    timeout: float,
    case: Case,
    print_content: bool,
    print_reasoning: bool,
) -> bool:
    print(f"\n=== {case.name} ===")
    if case.extra_body is not None:
        print("extra_body:", json.dumps(case.extra_body, indent=2, sort_keys=True))
    if case.reasoning_effort is not None:
        print("reasoning_effort:", case.reasoning_effort)

    try:
        request_kwargs: dict[str, Any] = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "timeout": timeout,
        }
        if case.reasoning_effort is not None:
            request_kwargs["reasoning_effort"] = case.reasoning_effort
        if case.extra_body is not None:
            request_kwargs["extra_body"] = case.extra_body

        raw = client.chat.completions.with_raw_response.create(**request_kwargs)
    except APIStatusError as e:
        print("ERROR:", type(e).__name__, e.status_code)
        if e.request_id:
            print("request_id:", e.request_id)
        if e.body is not None:
            print("body:", json.dumps(e.body, indent=2, sort_keys=True) if isinstance(e.body, dict) else repr(e.body))
        else:
            print("message:", str(e))
        return False
    except APIError as e:
        print("ERROR:", type(e).__name__)
        if e.body is not None:
            print("body:", json.dumps(e.body, indent=2, sort_keys=True) if isinstance(e.body, dict) else repr(e.body))
        else:
            print("message:", str(e))
        return False
    except Exception as e:
        print("ERROR:", type(e).__name__, repr(e))
        return False

    print("http_status:", raw.http_response.status_code)
    data = raw.http_response.json()
    _summarize_response(data, print_content=print_content, print_reasoning=print_reasoning)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke test OpenRouter reasoning controls (effort/max_tokens).")
    parser.add_argument(
        "--model",
        default="deepseek/deepseek-v3.2",
        help="OpenRouter model (default: deepseek/deepseek-v3.2).",
    )
    parser.add_argument(
        "--prompt",
        default="Which is bigger: 9.11 or 9.9? Answer with only the number.",
        help="Prompt to use for all cases.",
    )
    parser.add_argument("--max-tokens", type=int, default=256, help="Chat completion max_tokens (default: 256).")
    parser.add_argument("--temperature", type=float, default=0.0, help="Sampling temperature (default: 0.0).")
    parser.add_argument("--timeout", type=float, default=60.0, help="Request timeout in seconds (default: 60).")
    parser.add_argument("--print-content", action="store_true", help="Print assistant content verbatim.")
    parser.add_argument("--print-reasoning", action="store_true", help="Print assistant reasoning verbatim (if returned).")
    parser.add_argument(
        "--reasoning-max-tokens",
        type=int,
        default=64,
        help="Value used for the 'reasoning.max_tokens' case (default: 64).",
    )
    parser.add_argument(
        "--effort-min",
        choices=["xhigh", "high", "medium", "low", "minimal", "none"],
        default="minimal",
        help="Value used for the 'reasoning.effort' test case (default: minimal).",
    )
    parser.add_argument(
        "--effort-off",
        choices=["xhigh", "high", "medium", "low", "minimal", "none"],
        default="none",
        help="Value used for the 'reasoning.effort (off)' test case (default: none).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any case fails (default: only fail if the baseline call fails).",
    )
    args = parser.parse_args()

    load_env(override=True)
    client = _build_client()

    cases: list[Case] = [
        Case(name="baseline (no reasoning config)"),
        Case(
            name=f"openrouter reasoning.effort={args.effort_off}",
            extra_body={"reasoning": {"effort": args.effort_off}},
        ),
        Case(
            name=f"openrouter reasoning.effort={args.effort_min}",
            extra_body={"reasoning": {"effort": args.effort_min}},
        ),
        Case(
            name=f"openrouter reasoning.max_tokens={args.reasoning_max_tokens}",
            extra_body={"reasoning": {"max_tokens": args.reasoning_max_tokens}},
        ),
        Case(
            name="openai-style reasoning_effort=low (top-level param)",
            reasoning_effort="low",
        ),
    ]

    ok = []
    for case in cases:
        ok.append(
            _run_case(
                client,
                model=args.model,
                prompt=args.prompt,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                timeout=args.timeout,
                case=case,
                print_content=args.print_content,
                print_reasoning=args.print_reasoning,
            )
        )

    print("\n=== summary ===")
    for case, passed in zip(cases, ok, strict=True):
        print(f"{case.name}: {'OK' if passed else 'FAILED'}")

    if not ok or not ok[0]:
        return 2
    if args.strict and not all(ok):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
