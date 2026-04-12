"""
Run (or resume) a single run for the NO-EXPLANATION baseline on JAVA defects.

This is used for data-contamination control: comparing NO_EXPLANATION fix
success on original Java (Defects4J) vs. translated Python.

Output: results/<model_slug>/no_explanation_java/runs/java/
  - results_run{run_id}.json (thought process + raw fix, no validation)
  - per-defect fix artifacts: *_fix_raw.java, *_fix_thought.txt

No validation step — we cannot compile/run Java tests.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from scripts._common import load_env

from src.java_data import java_defects
from src.fix import FixGenerator
from src.llm import LLMService

load_env(override=True)


LEVELS_NAME = "NO_EXPLANATION"


def resolve_java_dir(results_dir: str) -> str:
    results_dir = results_dir.rstrip(os.sep)
    if os.path.basename(results_dir) == "java":
        return results_dir
    return os.path.join(results_dir, "java")


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
    parser = argparse.ArgumentParser(
        description="Run (or resume) one NO-EXPLANATION baseline run on JAVA defects"
    )
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
            "Results directory root. "
            "Default: results/<model_slug>/no_explanation_java/runs."
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
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned work and exit without LLM calls.",
    )
    parser.add_argument(
        "--defects",
        default=None,
        help=(
            "Optional comma-separated defect ids to run (e.g., defect1_java,defect2_java). "
            f"Default: all defects in src.java_data (currently {len(java_defects)})."
        ),
    )
    args = parser.parse_args()

    if args.model is None:
        args.model = "gpt-5-mini" if args.backend == "openai" else "deepseek/deepseek-v3.2"

    def slugify_model(m: str) -> str:
        name = m.split("/")[-1]
        return name.replace("-", "_").replace(".", "_")

    if args.results_dir is None:
        model_slug = slugify_model(args.model)
        args.results_dir = f"results/{model_slug}/no_explanation_java/runs"

    run_ids = args.run_ids if args.run_ids is not None else [args.run_id]
    if any(run_id <= 0 for run_id in run_ids):
        raise SystemExit("All run ids must be positive integers.")
    if len(set(run_ids)) != len(run_ids):
        raise SystemExit("Duplicate run ids are not allowed.")

    java_dir = resolve_java_dir(args.results_dir)

    selected_defects = java_defects
    if args.defects:
        wanted = {d.strip() for d in args.defects.split(",") if d.strip()}
        selected_defects = [d for d in java_defects if d.get("id") in wanted]
        missing = wanted - {d.get("id") for d in selected_defects}
        if missing:
            raise SystemExit(f"Unknown defect ids: {sorted(missing)}")

    if args.dry_run:
        print("backend:", args.backend)
        print("model:", args.model)
        print(f"java_dir: {java_dir}")
        print(f"run_ids: {run_ids}")
        print(f"defects: {len(selected_defects)}")
        print("levels: NO_EXPLANATION")
        return 0

    os.makedirs(java_dir, exist_ok=True)

    defect_order = {d.get("id"): idx for idx, d in enumerate(java_defects)}

    llm_service = LLMService(backend=args.backend, model=args.model)
    fix_generator = FixGenerator(llm_service)

    for run_id in run_ids:
        args.run_id = run_id
        results_path = os.path.join(java_dir, f"results_run{args.run_id}.json")

        existing_results = _load_existing_results(results_path)
        done_defects = {
            e.get("defect_id") for e in existing_results if e.get("levels") == LEVELS_NAME
        }

        total = len(selected_defects)
        completed = sum(1 for d in selected_defects if d.get("id") in done_defects)

        print(f"\n{'=' * 60}")
        print(f"JAVA NO-EXPLANATION RUN: run_id={args.run_id} | {len(selected_defects)} defects")
        print(f"Output: {java_dir}")
        print("Backend:", args.backend)
        print("Model:", args.model)
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

            source_path = defect.get("source_path")
            function_name = defect.get("function_name")

            # Read the Java source file
            with open(source_path, "r") as f:
                source_code = f.read()

            raw_path = os.path.join(
                java_dir, f"{defect_id}_{LEVELS_NAME}_run{args.run_id}_fix_raw.java"
            )
            thought_path = os.path.join(
                java_dir, f"{defect_id}_{LEVELS_NAME}_run{args.run_id}_fix_thought.txt"
            )

            try:
                # Generate fix (reuse if all artifacts exist)
                if not (os.path.exists(raw_path) and os.path.exists(thought_path)):
                    fix_result = fix_generator.generate_direct_java(source_code, function_name)
                    with open(raw_path, "w") as f:
                        f.write(fix_result["raw_fix"])
                    with open(thought_path, "w") as f:
                        f.write(fix_result["thought_process"])

                entry = {
                    "defect_id": defect_id,
                    "language": "java",
                    "levels": LEVELS_NAME,
                    "run_id": args.run_id,
                    "scores": None,
                    "fix_file": os.path.basename(raw_path),
                    "explanation_used": False,
                    "python_counterpart": defect.get("python_counterpart"),
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
        print(f"JAVA NO-EXPLANATION RUN COMPLETE: {datetime.now().strftime('%H:%M:%S')}")
        if appended:
            print(f"Wrote: {results_path} (+{appended} new entries)")
        else:
            print(f"No new entries (already complete): {results_path}")
        print(f"{'=' * 60}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
