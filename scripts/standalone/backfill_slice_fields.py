"""
Backfill slice metadata in existing results JSON files (no LLM calls).

This script is intended for cases where `slice_lines` and/or
`comparison.slice_coverage` are missing in already-generated runs.

It:
  - recomputes slice line sets deterministically via `src.experiment.Experiment`
  - fills top-level `slice_lines`
  - computes `comparison.slice_coverage` from:
      * comparison.expected_changed_lines
      * comparison.actual_changed_lines
      * slice_lines

By default it overwrites the original `results_run*.json` files, but always
creates a timestamped backup first.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# Add project root to sys.path before importing from scripts/src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src import python_defects  # noqa: E402
from src.experiment import ContextLevel, Experiment  # noqa: E402


SLICE_STRATEGIES: list[tuple[str, ContextLevel]] = [
    ("SLICE_BLOCK", ContextLevel.SLICE_BLOCK),
    ("SLICE_BACKWARD", ContextLevel.SLICE_BACKWARD),
    ("SLICE_FORWARD", ContextLevel.SLICE_FORWARD),
    ("SLICE_UNION", ContextLevel.SLICE_UNION),
]


def compute_slice_coverage(expected_lines: set[int], actual_lines: set[int], slice_lines: set[int]) -> dict:
    expected_covered = expected_lines & slice_lines
    actual_covered = actual_lines & slice_lines
    return {
        "expected_in_slice": len(expected_covered),
        "expected_total": len(expected_lines),
        "expected_coverage": (len(expected_covered) / len(expected_lines)) if expected_lines else 1.0,
        "actual_in_slice": len(actual_covered),
        "actual_total": len(actual_lines),
        "actual_coverage": (len(actual_covered) / len(actual_lines)) if actual_lines else 1.0,
    }


def _strategies_for_levels(levels: str) -> list[str]:
    if levels == "BASELINE":
        return [name for name, _ in SLICE_STRATEGIES]
    present: list[str] = []
    for name, _ in SLICE_STRATEGIES:
        if name in levels:
            present.append(name)
    return present


def _load_json_list(path: Path) -> list[dict]:
    data = json.loads(path.read_text())
    if not isinstance(data, list):
        raise ValueError(f"Expected a list in {path}, got {type(data).__name__}")
    return data


def _write_json_list(path: Path, data: list[dict]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(path)


@dataclass(frozen=True)
class BackfillStats:
    total: int
    slice_entries: int
    slice_lines_nonnull: int
    slice_coverage_nonnull: int
    empty_slice_sets: int


def backfill_results_file(results_path: Path, *, defect_map: dict[str, dict]) -> tuple[list[dict], BackfillStats]:
    results = _load_json_list(results_path)

    needed: dict[str, set[str]] = defaultdict(set)
    for entry in results:
        defect_id = entry.get("defect_id")
        levels = entry.get("levels") or ""
        if not defect_id:
            continue
        for strategy in _strategies_for_levels(levels):
            needed[defect_id].add(strategy)

    slice_cache: dict[tuple[str, str], list[int]] = {}
    empty_slice_sets = 0

    for defect_id, strategies in needed.items():
        defect = defect_map.get(defect_id)
        if defect is None:
            raise ValueError(f"Unknown defect_id in results: {defect_id}")
        exp = Experiment(defect)
        for strategy_name in sorted(strategies):
            level = dict(SLICE_STRATEGIES).get(strategy_name)
            if level is None:
                continue
            lines = sorted(list(exp.get_slice_lines(level)))
            if not lines:
                empty_slice_sets += 1
            slice_cache[(defect_id, strategy_name)] = lines

    slice_lines_nonnull = 0
    slice_coverage_nonnull = 0
    slice_entries = 0

    for entry in results:
        defect_id = entry.get("defect_id")
        levels = entry.get("levels") or ""
        if not defect_id:
            continue

        strategies = _strategies_for_levels(levels)
        if strategies:
            slice_entries += 1

        slice_lines_info: dict[str, list[int]] = {}
        for strategy in strategies:
            lines = slice_cache.get((defect_id, strategy))
            if lines is not None:
                slice_lines_info[strategy] = lines

        entry["slice_lines"] = slice_lines_info if slice_lines_info else None
        if entry["slice_lines"] is not None:
            slice_lines_nonnull += 1

        comparison = entry.get("comparison")
        if not isinstance(comparison, dict):
            continue

        if not slice_lines_info:
            comparison["slice_coverage"] = None
            continue

        expected = set(comparison.get("expected_changed_lines") or [])
        actual = set(comparison.get("actual_changed_lines") or [])

        slice_coverage: dict[str, dict] = {}
        for strategy, lines in slice_lines_info.items():
            slice_coverage[strategy] = compute_slice_coverage(expected, actual, set(lines))

        comparison["slice_coverage"] = slice_coverage
        slice_coverage_nonnull += 1

    stats = BackfillStats(
        total=len(results),
        slice_entries=slice_entries,
        slice_lines_nonnull=slice_lines_nonnull,
        slice_coverage_nonnull=slice_coverage_nonnull,
        empty_slice_sets=empty_slice_sets,
    )
    return results, stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Backfill slice_lines and comparison.slice_coverage")
    parser.add_argument(
        "--results-dir",
        required=True,
        help="Path to results python dir (e.g., results/gpt_5_mini/three_way/runs/python).",
    )
    parser.add_argument(
        "--runs",
        type=int,
        nargs="+",
        default=None,
        help="Run ids to backfill (e.g., --runs 1 2 3). Default: all results_run*.json found.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Disable timestamped backups (not recommended).",
    )
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    if not results_dir.exists() or not results_dir.is_dir():
        raise SystemExit(f"Not a directory: {results_dir}")

    all_paths = sorted(results_dir.glob("results_run*.json"))
    if not all_paths:
        raise SystemExit(f"No results_run*.json found under: {results_dir}")

    wanted_runs: set[int] | None = set(args.runs) if args.runs else None
    paths: list[Path] = []
    for p in all_paths:
        name = p.name
        try:
            run_id = int(name.replace("results_run", "").replace(".json", ""))
        except ValueError:
            continue
        if wanted_runs is None or run_id in wanted_runs:
            paths.append(p)

    if not paths:
        raise SystemExit("No matching runs selected.")

    defect_map = {d.get("id"): d for d in python_defects if d.get("id")}
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    print(f"Results dir: {results_dir}")
    print(f"Files: {len(paths)}")
    for p in paths:
        print(f"  - {p.name}")

    for p in paths:
        if not args.no_backup:
            backup = p.with_suffix(p.suffix + f".bak.{timestamp}")
            shutil.copy2(p, backup)
            print(f"Backup: {backup.name}")

        updated_results, stats = backfill_results_file(p, defect_map=defect_map)
        _write_json_list(p, updated_results)

        # Re-load to ensure the file is valid JSON after write
        results = _load_json_list(p)
        # Basic summary from computed stats (more reliable than scanning twice here)
        print(
            f"Backfilled: {p.name} | entries={stats.total} | "
            f"slice-level entries={stats.slice_entries} | "
            f"slice_lines non-null={stats.slice_lines_nonnull} | "
            f"slice_coverage non-null={stats.slice_coverage_nonnull} | "
            f"empty slice sets={stats.empty_slice_sets}"
        )

        # sanity: keep counts deterministic and catch accidental schema breakage
        if len(results) != stats.total:
            raise SystemExit(f"Unexpected entry count change in {p.name}")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
