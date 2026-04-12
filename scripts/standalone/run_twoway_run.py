"""
Run (or resume) a single run for all two-way context combinations (+ BASELINE).

This script writes directly into `results/<model_slug>/two_way/runs/python/` by default, so it can
be used without moving artifacts after execution.

Default behavior:
  - all defects (src.python_defects)
  - 28 two-way combinations of the 8 isolated context levels
  - + BASELINE (all isolated levels OR'ed) appended last (29 configs total)
  - run_id = 1
  - writes to: results/<model_slug>/two_way/runs/python/

Resume support:
  - If results_run{run_id}.json exists, completed (defect_id, levels) pairs are skipped.
  - Existing explanation/fix artifacts for run_id are reused when present.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from itertools import combinations

# Add project root to sys.path before importing from scripts/src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from scripts._common import load_env

from src import python_defects
from src.evaluation import ExplanationEvaluator
from src.experiment import ContextLevel, Experiment
from src.fix import FixGenerator
from src.llm import LLMService
from src.validation import FixValidator

load_env(override=True)


ISOLATED_LEVELS: list[ContextLevel] = [
    ContextLevel.CODE,
    ContextLevel.ERROR,
    ContextLevel.TEST,
    ContextLevel.DOCSTRING,
    ContextLevel.SLICE_BLOCK,
    ContextLevel.SLICE_BACKWARD,
    ContextLevel.SLICE_FORWARD,
    ContextLevel.SLICE_UNION,
]


def _baseline_config() -> ContextLevel:
    config = ContextLevel.NONE
    for level in ISOLATED_LEVELS:
        config |= level
    return config


def build_twoway_level_configs(*, include_baseline: bool = True) -> list[ContextLevel]:
    configs: list[ContextLevel] = []
    for a, b in combinations(ISOLATED_LEVELS, 2):
        configs.append(a | b)
    if include_baseline:
        configs.append(_baseline_config())
    return configs


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


def _sort_results_in_place(
    results: list[dict],
    *,
    defect_order: dict[str, int],
    config_order: dict[str, int],
) -> None:
    def sort_key(entry: dict) -> tuple[int, int]:
        defect_id = entry.get("defect_id", "")
        levels = entry.get("levels", "")
        return (defect_order.get(defect_id, 10**9), config_order.get(levels, 10**9))

    results.sort(key=sort_key)


def _collect_slice_lines(exp: Experiment, levels: ContextLevel) -> dict[str, list[int]] | None:
    slice_lines_info: dict[str, list[int]] = {}
    for slice_level in [
        ContextLevel.SLICE_BLOCK,
        ContextLevel.SLICE_BACKWARD,
        ContextLevel.SLICE_FORWARD,
        ContextLevel.SLICE_UNION,
    ]:
        if slice_level in levels:
            slice_lines_info[slice_level.name] = sorted(list(exp.get_slice_lines(slice_level)))
    return slice_lines_info if slice_lines_info else None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run (or resume) a single run for all 2-way combinations (+ BASELINE)"
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
            "Results directory root. Can also be the python dir. "
            "Default: results/<model_slug>/two_way/runs (e.g., results/gpt_5_mini/two_way/runs, "
            "results/deepseek_v3_2/two_way/runs, results/grok_4_1_fast/two_way/runs)."
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
        help="Print planned configs and exit without LLM calls.",
    )
    parser.add_argument(
        "--defects",
        default=None,
        help=(
            "Optional comma-separated defect ids to run (e.g., defect1_py,defect2_py). "
            f"Default: all defects in src.python_defects (currently {len(python_defects)})."
        ),
    )
    gt_group = parser.add_mutually_exclusive_group()
    gt_group.add_argument(
        "--compare-gt",
        dest="compare_gt",
        action="store_true",
        help="Compute and store per-entry ground-truth comparison (enabled by default).",
    )
    gt_group.add_argument(
        "--no-compare-gt",
        dest="compare_gt",
        action="store_false",
        help="Disable ground-truth comparison.",
    )
    parser.set_defaults(compare_gt=True)
    args = parser.parse_args()

    if args.model is None:
        args.model = "gpt-5-mini" if args.backend == "openai" else "deepseek/deepseek-v3.2"

    def slugify_model(m: str) -> str:
        name = m.split("/")[-1]
        return name.replace("-", "_").replace(".", "_")

    if args.results_dir is None:
        model_slug = slugify_model(args.model)
        args.results_dir = f"results/{model_slug}/two_way/runs"

    run_ids = args.run_ids if args.run_ids is not None else [args.run_id]
    if any(run_id <= 0 for run_id in run_ids):
        raise SystemExit("All run ids must be positive integers.")
    if len(set(run_ids)) != len(run_ids):
        raise SystemExit("Duplicate run ids are not allowed.")

    python_dir = resolve_python_dir(args.results_dir)

    level_configs = build_twoway_level_configs(include_baseline=True)
    config_names = [Experiment.levels_to_string(c) for c in level_configs]

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
        print("compare_gt:", "on" if args.compare_gt else "off")
        print(f"defects: {len(selected_defects)}")
        print(f"configs: {len(level_configs)}")
        print("config list:")
        for name in config_names:
            print(f"  - {name}")
        return 0

    os.makedirs(python_dir, exist_ok=True)

    compare_with_ground_truth = None
    if args.compare_gt:
        from scripts.generate_report import compare_with_ground_truth as _compare_with_ground_truth

        compare_with_ground_truth = _compare_with_ground_truth

    defect_order = {d.get("id"): idx for idx, d in enumerate(python_defects)}
    config_order = {name: idx for idx, name in enumerate(config_names)}

    llm_service = LLMService(backend=args.backend, model=args.model)
    evaluator = ExplanationEvaluator(llm_service)
    fix_generator = FixGenerator(llm_service)
    validator = FixValidator()

    for run_id in run_ids:
        args.run_id = run_id
        results_path = os.path.join(python_dir, f"results_run{args.run_id}.json")

        existing_results = _load_existing_results(results_path)
        done_pairs = {(e.get("defect_id"), e.get("levels")) for e in existing_results}

        total = len(selected_defects) * len(level_configs)
        completed = sum(
            1 for d in selected_defects for n in config_names if (d.get("id"), n) in done_pairs
        )

        print(f"\n{'=' * 60}")
        print(
            f"TWO-WAY RUN: run_id={args.run_id} | {len(selected_defects)} defects | {len(level_configs)} configs"
        )
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
            ground_truth = defect.get("ground_truth", "")
            function_name = defect.get("function_name")

            exp = Experiment(defect)

            for levels in level_configs:
                levels_name = Experiment.levels_to_string(levels)
                if (defect_id, levels_name) in done_pairs:
                    continue

                label = f"{defect_id}/{levels_name}"
                print(f"  {label}...", end=" ", flush=True)

                explanation_path = os.path.join(
                    python_dir, f"{defect_id}_{levels_name}_run{args.run_id}.txt"
                )
                fix_path = os.path.join(
                    python_dir, f"{defect_id}_{levels_name}_run{args.run_id}_fix.py"
                )
                raw_path = os.path.join(
                    python_dir, f"{defect_id}_{levels_name}_run{args.run_id}_fix_raw.py"
                )
                thought_path = os.path.join(
                    python_dir, f"{defect_id}_{levels_name}_run{args.run_id}_fix_thought.txt"
                )

                try:
                    # Explanation (reuse if already present)
                    if os.path.exists(explanation_path):
                        with open(explanation_path, "r") as f:
                            explanation = f.read()
                    else:
                        explanation = exp.run(levels, llm_service)
                        with open(explanation_path, "w") as f:
                            f.write(explanation)

                    # Fix (reuse if all artifacts exist)
                    if not (
                        os.path.exists(fix_path)
                        and os.path.exists(raw_path)
                        and os.path.exists(thought_path)
                    ):
                        fix_result = fix_generator.generate(
                            exp.source_code, explanation, function_name=function_name
                        )
                        with open(fix_path, "w") as f:
                            f.write(fix_result["code"])
                        with open(raw_path, "w") as f:
                            f.write(fix_result["raw_fix"])
                        with open(thought_path, "w") as f:
                            f.write(fix_result["thought_process"])

                    # Evaluate explanation
                    scores = evaluator.evaluate(explanation, ground_truth)

                    # Slice line numbers for any slice strategies used
                    slice_lines = _collect_slice_lines(exp, levels)

                    # Validate fix (graceful failure)
                    try:
                        original_module_name = os.path.splitext(os.path.basename(defect["source_path"]))[
                            0
                        ]
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

                    entry = {
                        "defect_id": defect_id,
                        "language": "python",
                        "levels": levels_name,
                        "run_id": args.run_id,
                        "scores": scores,
                        "explanation_used": True,
                        "fix_file": os.path.basename(fix_path),
                        "slice_lines": slice_lines,
                        "validation": validation,
                        "comparison": None,
                    }

                    if compare_with_ground_truth is not None:
                        entry["comparison"] = compare_with_ground_truth(
                            defect_id, python_dir, os.path.basename(fix_path), slice_lines
                        )

                    existing_results.append(entry)
                    done_pairs.add((defect_id, levels_name))
                    appended += 1

                    _sort_results_in_place(
                        existing_results, defect_order=defect_order, config_order=config_order
                    )
                    _write_results(results_path, existing_results)
                    print("✓")
                except Exception as e:
                    print(f"✗ {e}")

        print(f"\n{'=' * 60}")
        print(f"TWO-WAY RUN COMPLETE: {datetime.now().strftime('%H:%M:%S')}")
        if appended:
            print(f"Wrote: {results_path} (+{appended} new entries)")
        else:
            print(f"No new entries (already complete): {results_path}")
        print(f"{'=' * 60}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
