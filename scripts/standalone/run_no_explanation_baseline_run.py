"""
Run (or resume) a single run for the no-explanation baseline (direct fix only).

This script writes directly into `results/<model_slug>/no_explanation/runs/python/` by default.

Behavior:
  - all defects (src.python_defects)
  - levels = NO_EXPLANATION
  - scores = None
  - explanation_used = False
  - run_id = 1
  - writes to: results/<model_slug>/no_explanation/runs/python/

Resume support:
  - If results_run{run_id}.json exists, completed defects are skipped.
  - Existing fix artifacts for run_id are reused when present.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime

# Add project root to sys.path before importing from scripts/src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from scripts._common import load_env

from src import python_defects
from src.experiment import Experiment
from src.fix import FixGenerator
from src.llm import LLMService
from src.validation import FixValidator

load_env(override=True)


LEVELS_NAME = "NO_EXPLANATION"


def resolve_python_dir(results_dir: str) -> str:
    results_dir = results_dir.rstrip(os.sep)
    if os.path.basename(results_dir) == "python":
        return results_dir
    return os.path.join(results_dir, "python")


def _load_existing_results(results_path: str) -> list[dict]:
    if not os.path.exists(results_path):
        return []
    with open(results_path, "r") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"Expected a list in {results_path}, got {type(data).__name__}")
    return data


def _write_results(results_path: str, results: list[dict]) -> None:
    tmp_path = results_path + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(results, f, indent=2)
    os.replace(tmp_path, results_path)


def _sort_results_in_place(results: list[dict], *, defect_order: dict[str, int]) -> None:
    def sort_key(entry: dict) -> int:
        defect_id = entry.get("defect_id", "")
        return defect_order.get(defect_id, 10**9)

    results.sort(key=sort_key)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run (or resume) one NO-EXPLANATION baseline run")
    parser.add_argument(
        "--backend",
        choices=["openai", "openrouter"],
        default="openai",
        help="LLM backend (default: openai).",
    )
    parser.add_argument(
        "--model",
        default=None,
        help=(
            "Model name (default: gpt-5-mini for openai; deepseek/deepseek-v3.2 for openrouter). "
            "Example OpenRouter models: deepseek/deepseek-v3.2, x-ai/grok-4.1-fast."
        ),
    )
    parser.add_argument(
        "--results-dir",
        default=None,
        help=(
            "Results directory root. Can also be the python dir. "
            "Default: results/<model_slug>/no_explanation/runs (e.g., results/gpt_5_mini/no_explanation/runs, "
            "results/deepseek_v3_2/no_explanation/runs, results/grok_4_1_fast/no_explanation/runs)."
        ),
    )
    run_group = parser.add_mutually_exclusive_group()
    run_group.add_argument(
        "--run-id",
        type=int,
        default=1,
        help="Run id to generate (default: 1).",
    )
    run_group.add_argument(
        "--run-ids",
        type=int,
        nargs="+",
        default=None,
        help="One or more run ids (e.g., --run-ids 1 2 3).",
    )
    gt_group = parser.add_mutually_exclusive_group()
    gt_group.add_argument(
        "--compare-gt",
        dest="compare_gt",
        action="store_true",
        help="Enable ground-truth comparison (enabled by default to match existing 38_01 schema).",
    )
    gt_group.add_argument(
        "--no-compare-gt",
        dest="compare_gt",
        action="store_false",
        help="Disable ground-truth comparison.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned work and exit without LLM calls.",
    )
    parser.add_argument(
        "--defects",
        default=None,
        help=(
            "Optional comma-separated defect ids to run (e.g., defect1_py,defect2_py). "
            f"Default: all defects in src.python_defects (currently {len(python_defects)})."
        ),
    )
    parser.set_defaults(compare_gt=True)
    args = parser.parse_args()

    if args.model is None:
        args.model = "gpt-5-mini" if args.backend == "openai" else "deepseek/deepseek-v3.2"

    def slugify_model(m: str) -> str:
        # e.g. "deepseek/deepseek-v3.2" -> "deepseek_v3_2" or "gpt-5-mini" -> "gpt_5_mini"
        # We'll take the basename if it has a slash, then replace dots and dashes.
        name = m.split("/")[-1]
        return name.replace("-", "_").replace(".", "_")

    if args.results_dir is None:
        model_slug = slugify_model(args.model)
        args.results_dir = f"results/{model_slug}/no_explanation/runs"

    run_ids = args.run_ids if args.run_ids is not None else [args.run_id]
    if any(run_id <= 0 for run_id in run_ids):
        raise SystemExit("All run ids must be positive integers.")
    if len(set(run_ids)) != len(run_ids):
        raise SystemExit("Duplicate run ids are not allowed.")

    python_dir = resolve_python_dir(args.results_dir)

    selected_defects = python_defects
    if args.defects:
        wanted = {d.strip() for d in args.defects.split(",") if d.strip()}
        selected_defects = [d for d in python_defects if d.get("id") in wanted]
        missing = wanted - {d.get("id") for d in selected_defects}
        if missing:
            raise SystemExit(f"Unknown defect ids: {sorted(missing)}")

    if args.dry_run:
        print("backend:", args.backend)
        print("model:", args.model)
        print(f"python_dir: {python_dir}")
        print(f"run_ids: {run_ids}")
        print(f"defects: {len(selected_defects)}")
        print("levels: NO_EXPLANATION")
        print("compare_gt:", "on" if args.compare_gt else "off")
        return 0

    os.makedirs(python_dir, exist_ok=True)

    compare_with_ground_truth = None
    if args.compare_gt:
        from scripts.generate_report import compare_with_ground_truth as _compare_with_ground_truth

        compare_with_ground_truth = _compare_with_ground_truth

    defect_order = {d.get("id"): idx for idx, d in enumerate(python_defects)}

    llm_service = LLMService(backend=args.backend, model=args.model)
    fix_generator = FixGenerator(llm_service)
    validator = FixValidator()

    for run_id in run_ids:
        args.run_id = run_id
        results_path = os.path.join(python_dir, f"results_run{args.run_id}.json")

        existing_results = _load_existing_results(results_path)
        done_defects = {
            e.get("defect_id") for e in existing_results if e.get("levels") == LEVELS_NAME
        }

        total = len(selected_defects)
        completed = sum(1 for d in selected_defects if d.get("id") in done_defects)

        print(f"\n{'=' * 60}")
        print(f"NO-EXPLANATION RUN: run_id={args.run_id} | {len(selected_defects)} defects")
        print(f"Output: {python_dir}")
        print("Backend:", args.backend)
        print("Model:", args.model)
        print("Compare GT:", "on" if args.compare_gt else "off")
        print(f"Progress: {completed}/{total} already complete (resume)")
        print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'=' * 60}\n")

        appended = 0

        for defect in selected_defects:
            defect_id = defect.get("id")
            if not defect_id:
                continue
            if defect_id in done_defects:
                continue

            label = f"{defect_id}/{LEVELS_NAME}"
            print(f"  {label}...", end=" ", flush=True)

            exp = Experiment(defect)
            function_name = defect.get("function_name")

            fix_path = os.path.join(python_dir, f"{defect_id}_{LEVELS_NAME}_run{args.run_id}_fix.py")
            raw_path = os.path.join(
                python_dir, f"{defect_id}_{LEVELS_NAME}_run{args.run_id}_fix_raw.py"
            )
            thought_path = os.path.join(
                python_dir, f"{defect_id}_{LEVELS_NAME}_run{args.run_id}_fix_thought.txt"
            )

            try:
                # Generate fix (reuse if all artifacts exist)
                if not (
                    os.path.exists(fix_path) and os.path.exists(raw_path) and os.path.exists(thought_path)
                ):
                    fix_result = fix_generator.generate_direct(exp.source_code, function_name)
                    with open(fix_path, "w") as f:
                        f.write(fix_result["code"])
                    with open(raw_path, "w") as f:
                        f.write(fix_result["raw_fix"])
                    with open(thought_path, "w") as f:
                        f.write(fix_result["thought_process"])

                # Validate fix (graceful failure)
                try:
                    original_module_name = os.path.splitext(os.path.basename(defect["source_path"]))[0]
                    validation_result = validator.validate(
                        fix_path=fix_path,
                        test_path=defect["test_path"],
                        module_name=original_module_name,
                    )
                    validation = {
                        "passed": validation_result.get("passed", False),
                        "output": validation_result.get("output", ""),
                        "error": validation_result.get("error", ""),
                    }
                except Exception as ve:
                    validation = {"passed": False, "output": "", "error": f"Harness Error: {str(ve)}"}

                comparison = None
                if compare_with_ground_truth is not None:
                    comparison = compare_with_ground_truth(
                        defect_id, python_dir, os.path.basename(fix_path), None
                    )

                entry = {
                    "defect_id": defect_id,
                    "language": "python",
                    "levels": LEVELS_NAME,
                    "run_id": args.run_id,
                    "scores": None,
                    "fix_file": os.path.basename(fix_path),
                    "slice_lines": None,
                    "explanation_used": False,
                    "validation": validation,
                    "comparison": comparison,
                }

                existing_results.append(entry)
                done_defects.add(defect_id)
                appended += 1

                _sort_results_in_place(existing_results, defect_order=defect_order)
                _write_results(results_path, existing_results)
                print("✓")
            except Exception as e:
                print(f"✗ {e}")

        print(f"\n{'=' * 60}")
        print(f"NO-EXPLANATION RUN COMPLETE: {datetime.now().strftime('%H:%M:%S')}")
        if appended:
            print(f"Wrote: {results_path} (+{appended} new entries)")
        else:
            print(f"No new entries (already complete): {results_path}")
        print(f"{'=' * 60}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
