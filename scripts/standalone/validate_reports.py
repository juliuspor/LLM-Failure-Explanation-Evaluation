#!/usr/bin/env python3
"""
Validate that generated CSV reports accurately reflect pipeline JSON results.

This script independently recalculates all values from the raw JSON results
and compares them against the generated CSV files to ensure accuracy.

Usage:
    python scripts/validate_reports.py results/gpt_5_mini/three_way
"""

import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev


CRITERIA = [
    "C1_Readability",
    "C2_Problem_Identification", 
    "C3_Explanation_Clarity",
    "C4_Actionability",
    "C5_Contextual_Adequacy",
    "C6_Brevity"
]

TOLERANCE = 0.001  # Floating point comparison tolerance


def load_json_results(results_folder: Path) -> list:
    """Load all results_run*.json files from runs/python/ directory."""
    runs_path = results_folder / "runs" / "python"
    
    if not runs_path.exists():
        print(f"Error: Runs directory not found: {runs_path}")
        return []
    
    all_results = []
    json_files = sorted(runs_path.glob("results_run*.json"))
    
    if not json_files:
        print(f"Error: No results_run*.json files found in {runs_path}")
        return []
    
    for json_file in json_files:
        with open(json_file) as f:
            results = json.load(f)
            all_results.extend(results)
            print(f"  Loaded {len(results)} entries from {json_file.name}")
    
    return all_results


def load_csv(filepath: Path) -> list[dict]:
    """Load CSV file into list of dicts."""
    if not filepath.exists():
        return []
    
    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)


def values_match(expected: float, found: float, tolerance: float = TOLERANCE) -> bool:
    """Check if two float values match within tolerance."""
    return abs(expected - found) <= tolerance


def validate_comparison_csv(results: list, csv_path: Path) -> tuple[bool, list[str]]:
    """
    Validate comparison.csv against recalculated values.
    
    Returns:
        (passed, messages): Boolean success and list of messages
    """
    messages = []
    csv_data = load_csv(csv_path)
    
    if not csv_data:
        return False, [f"Could not load {csv_path}"]
    
    # Recalculate: group scores by level and criterion
    grouped = defaultdict(lambda: defaultdict(list))
    for entry in results:
        level = entry.get("levels", "unknown")
        scores = entry.get("scores", {})
        for criterion in CRITERIA:
            if criterion in scores:
                grouped[level][criterion].append(scores[criterion])
    
    # Calculate expected values
    expected = {}
    for level in grouped:
        expected[level] = {}
        for criterion in CRITERIA:
            values = grouped[level].get(criterion, [])
            if values:
                expected[level][criterion] = {
                    "mean": round(mean(values), 3),
                    "std": round(stdev(values), 3) if len(values) > 1 else 0.0
                }
            else:
                expected[level][criterion] = {"mean": 0.0, "std": 0.0}
    
    # Compare against CSV
    discrepancies = []
    values_checked = 0
    
    for row_idx, row in enumerate(csv_data, start=2):  # Start at 2 (header is row 1)
        level = row.get("Levels", "")
        criterion = row.get("Criterion", "")
        csv_mean = float(row.get("Mean", 0))
        csv_std = float(row.get("Std", 0))
        
        exp = expected.get(level, {}).get(criterion, {"mean": 0.0, "std": 0.0})
        exp_mean = exp["mean"]
        exp_std = exp["std"]
        
        values_checked += 2  # Mean and Std
        
        if not values_match(exp_mean, csv_mean):
            discrepancies.append(
                f"  Row {row_idx}: Level={level}, Criterion={criterion}\n"
                f"    Mean: expected {exp_mean:.3f}, found {csv_mean:.3f} "
                f"(diff: {abs(exp_mean - csv_mean):.4f})"
            )
        
        if not values_match(exp_std, csv_std):
            discrepancies.append(
                f"  Row {row_idx}: Level={level}, Criterion={criterion}\n"
                f"    Std: expected {exp_std:.3f}, found {csv_std:.3f} "
                f"(diff: {abs(exp_std - csv_std):.4f})"
            )
    
    # Build result messages
    levels_count = len(set(row.get("Levels") for row in csv_data))
    messages.append(f"  Checked {values_checked} values across {levels_count} levels × {len(CRITERIA)} criteria")
    
    if discrepancies:
        messages.append(f"  ✗ Found {len(discrepancies)} discrepancies:")
        messages.extend(discrepancies)
        return False, messages
    else:
        messages.append(f"  ✓ All means and stds match within tolerance ({TOLERANCE})")
        return True, messages


def validate_defect_breakdown_csv(results: list, csv_path: Path) -> tuple[bool, list[str]]:
    """
    Validate defect_breakdown.csv against recalculated values.
    
    Returns:
        (passed, messages): Boolean success and list of messages
    """
    messages = []
    csv_data = load_csv(csv_path)
    
    if not csv_data:
        return False, [f"Could not load {csv_path}"]
    
    # Recalculate: group scores by defect_id, level, criterion
    grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for entry in results:
        defect_id = entry.get("defect_id", "unknown")
        level = entry.get("levels", "unknown")
        scores = entry.get("scores", {})
        for criterion in CRITERIA:
            if criterion in scores:
                grouped[defect_id][level][criterion].append(scores[criterion])
    
    # Calculate expected values
    expected = {}
    for defect_id in grouped:
        expected[defect_id] = {}
        for level in grouped[defect_id]:
            expected[defect_id][level] = {}
            for criterion in CRITERIA:
                values = grouped[defect_id][level].get(criterion, [])
                if values:
                    expected[defect_id][level][criterion] = round(mean(values), 3)
                else:
                    expected[defect_id][level][criterion] = 0.0
    
    # Compare against CSV
    discrepancies = []
    values_checked = 0
    
    for row_idx, row in enumerate(csv_data, start=2):
        defect = row.get("Defect", "")
        level = row.get("Levels", "")
        
        for criterion in CRITERIA:
            csv_value = float(row.get(criterion, 0))
            exp_value = expected.get(defect, {}).get(level, {}).get(criterion, 0.0)
            values_checked += 1
            
            if not values_match(exp_value, csv_value):
                discrepancies.append(
                    f"  Row {row_idx}: Defect={defect}, Level={level}, {criterion}\n"
                    f"    Expected {exp_value:.3f}, found {csv_value:.3f} "
                    f"(diff: {abs(exp_value - csv_value):.4f})"
                )
    
    # Build result messages
    defects_count = len(set(row.get("Defect") for row in csv_data))
    levels_count = len(set(row.get("Levels") for row in csv_data))
    messages.append(f"  Checked {values_checked} values across {defects_count} defects × {levels_count} levels × {len(CRITERIA)} criteria")
    
    if discrepancies:
        messages.append(f"  ✗ Found {len(discrepancies)} discrepancies:")
        messages.extend(discrepancies[:10])  # Limit output
        if len(discrepancies) > 10:
            messages.append(f"  ... and {len(discrepancies) - 10} more")
        return False, messages
    else:
        messages.append(f"  ✓ All values match within tolerance ({TOLERANCE})")
        return True, messages


def validate_fix_results_csv(results: list, csv_path: Path) -> tuple[bool, list[str]]:
    """
    Validate fix_results.csv against recalculated values.
    
    Returns:
        (passed, messages): Boolean success and list of messages
    """
    messages = []
    csv_data = load_csv(csv_path)
    
    if not csv_data:
        return False, [f"Could not load {csv_path}"]
    
    # Recalculate: count passed/failed per level
    grouped = defaultdict(lambda: {"passed": 0, "failed": 0, "total": 0})
    
    for entry in results:
        level = entry.get("levels", "unknown")
        # Backward compatibility: check for 'validation' then 'verification'
        validation = entry.get("validation") or entry.get("verification", {})
        
        if validation:
            grouped[level]["total"] += 1
            if validation.get("passed", False):
                grouped[level]["passed"] += 1
            else:
                grouped[level]["failed"] += 1
    
    # Compare against CSV
    discrepancies = []
    levels_checked = 0
    
    for row_idx, row in enumerate(csv_data, start=2):
        level = row.get("Level", "")
        csv_passed = int(row.get("Passed", 0))
        csv_failed = int(row.get("Failed", 0))
        csv_total = int(row.get("Total", 0))
        csv_rate = float(row.get("Pass_Rate", 0))
        
        exp = grouped.get(level, {"passed": 0, "failed": 0, "total": 0})
        exp_passed = exp["passed"]
        exp_failed = exp["failed"]
        exp_total = exp["total"]
        exp_rate = round(exp_passed / exp_total, 3) if exp_total > 0 else 0.0
        
        levels_checked += 1
        
        # Check exact counts
        if exp_passed != csv_passed:
            discrepancies.append(
                f"  Row {row_idx}: Level={level}\n"
                f"    Passed: expected {exp_passed}, found {csv_passed}"
            )
        
        if exp_failed != csv_failed:
            discrepancies.append(
                f"  Row {row_idx}: Level={level}\n"
                f"    Failed: expected {exp_failed}, found {csv_failed}"
            )
        
        if exp_total != csv_total:
            discrepancies.append(
                f"  Row {row_idx}: Level={level}\n"
                f"    Total: expected {exp_total}, found {csv_total}"
            )
        
        if not values_match(exp_rate, csv_rate):
            discrepancies.append(
                f"  Row {row_idx}: Level={level}\n"
                f"    Pass_Rate: expected {exp_rate:.3f}, found {csv_rate:.3f}"
            )
    
    # Build result messages
    messages.append(f"  Checked {levels_checked} levels")
    
    if discrepancies:
        messages.append(f"  ✗ Found {len(discrepancies)} discrepancies:")
        messages.extend(discrepancies)
        return False, messages
    else:
        messages.append(f"  ✓ All counts and rates match exactly")
        return True, messages


def main():
    parser = argparse.ArgumentParser(
        description="Validate CSV reports against JSON pipeline results.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/validate_reports.py results/gpt_5_mini/three_way
    python scripts/validate_reports.py results/34_01
        """
    )
    parser.add_argument(
        "results_folder",
        type=str,
        help="Path to results folder (e.g., results/gpt_5_mini/three_way)"
    )
    
    args = parser.parse_args()
    results_folder = Path(args.results_folder)
    
    # Validate path exists
    if not results_folder.exists():
        print(f"Error: Results folder not found: {results_folder}")
        sys.exit(2)
    
    reports_path = results_folder / "reports"
    if not reports_path.exists():
        print(f"Error: Reports directory not found: {reports_path}")
        sys.exit(2)
    
    print(f"\nValidating: {results_folder}\n")
    print("Loading JSON results...")
    results = load_json_results(results_folder)
    
    if not results:
        print("Error: No results loaded")
        sys.exit(2)
    
    print(f"Total entries loaded: {len(results)}\n")
    
    # Track overall status
    all_passed = True
    
    # Validate comparison.csv
    print("=" * 50)
    print("[comparison.csv]")
    comparison_path = reports_path / "comparison.csv"
    passed, messages = validate_comparison_csv(results, comparison_path)
    for msg in messages:
        print(msg)
    if not passed:
        all_passed = False
    print()
    
    # Validate defect_breakdown.csv
    print("=" * 50)
    print("[defect_breakdown.csv]")
    defect_path = reports_path / "defect_breakdown.csv"
    passed, messages = validate_defect_breakdown_csv(results, defect_path)
    for msg in messages:
        print(msg)
    if not passed:
        all_passed = False
    print()
    
    # Validate fix_results.csv
    print("=" * 50)
    print("[fix_results.csv]")
    fix_path = reports_path / "fix_results.csv"
    passed, messages = validate_fix_results_csv(results, fix_path)
    for msg in messages:
        print(msg)
    if not passed:
        all_passed = False
    print()
    
    # Final summary
    print("=" * 50)
    if all_passed:
        print("RESULT: All validations passed ✓")
        print("=" * 50)
        sys.exit(0)
    else:
        print("RESULT: Validation FAILED ✗")
        print("=" * 50)
        sys.exit(1)


if __name__ == "__main__":
    main()
