"""
Generate comparison report and visualizations for evaluation results.
"""

import os
import json
import argparse
from collections import defaultdict
from statistics import mean, stdev

import matplotlib

# Avoid macOS GUI backend crashes when generating/saving plots from a CLI script.
# Users can still override via MPLBACKEND env var.
if os.environ.get("MPLBACKEND") is None:
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from difflib import unified_diff, SequenceMatcher

# Add project root to sys.path before importing from scripts/src
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ast
from src import normalize_python_code
from src.data import python_defects
from radon.metrics import h_visit
from scripts.explanation_metrics import run_explanation_metrics


RESULTS_DIR = "results/runs"
REPORTS_DIR = "results/reports"
MINIMAL_FIX_DIR = "failures/python_defects/minimal_fix"
CRITERIA = ["C1_Readability", "C2_Problem_Identification", "C3_Explanation_Clarity", 
            "C4_Actionability", "C5_Contextual_Adequacy", "C6_Brevity"]


def resolve_reports_dir(python_path: str) -> str:
    """
    Resolve a stable reports directory based on the discovered python results path.

    - If python_path is .../runs/python, write reports to .../reports
    - Otherwise, write reports next to python_path as .../reports
    """
    python_path = python_path.rstrip(os.sep)
    parent_dir = os.path.dirname(python_path)
    if os.path.basename(parent_dir) == "runs":
        return os.path.join(os.path.dirname(parent_dir), "reports")
    return os.path.join(parent_dir, "reports")


def _find_function_node(tree: ast.AST, function_name: str):
    """Find a function/method node by name (supports 'Class.method' format)."""
    parts = function_name.split(".")
    
    if len(parts) == 2:
        class_name, method_name = parts
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == method_name:
                        return item
    else:
        func_name = parts[0]
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func_name:
                return node
    return None


def _extract_function_with_line_mapping(source_code: str, function_name: str) -> list:
    """
    Extract function code (excluding docstring) with source line number mapping.
    Includes decorators if present.
    
    Returns:
        List of tuples: [(source_line_num, code_line), ...]
        Empty list if function not found.
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return []
    
    target_node = _find_function_node(tree, function_name)
    if target_node is None:
        return []
    
    source_lines = source_code.splitlines()
    
    # Include decorators - they come before lineno
    if target_node.decorator_list:
        start_line = min(dec.lineno for dec in target_node.decorator_list)
    else:
        start_line = target_node.lineno
    
    end_line = target_node.end_lineno
    
    extracted = []
    
    # Check if function has a docstring
    has_docstring = (
        target_node.body and 
        isinstance(target_node.body[0], ast.Expr) and 
        isinstance(target_node.body[0].value, ast.Constant) and 
        isinstance(target_node.body[0].value.value, str)
    )
    
    if has_docstring:
        docstring_start = target_node.body[0].lineno
        docstring_end = target_node.body[0].end_lineno
        
        # Include decorators + signature lines (before docstring)
        for i in range(start_line, docstring_start):
            extracted.append((i, source_lines[i - 1]))
        
        # Skip docstring, include body lines (after docstring)
        for i in range(docstring_end + 1, end_line + 1):
            extracted.append((i, source_lines[i - 1]))
    else:
        # No docstring, include all lines (decorators + function)
        for i in range(start_line, end_line + 1):
            extracted.append((i, source_lines[i - 1]))
    
    return extracted


def compute_halstead_volume_effort(code: str) -> tuple[float | None, float | None]:
    """
    Compute Halstead Volume and Effort metrics using radon.
    
    Args:
        code: Python source code string
    
    Returns:
        Tuple of (volume, effort) or (None, None) if computation fails
    """
    try:
        halstead = h_visit(code)
        # h_visit returns a Halstead object with 'total' and 'functions' attributes
        # Use total metrics (aggregated across all functions)
        if hasattr(halstead, 'total') and halstead.total:
            volume = halstead.total.volume
            effort = halstead.total.effort
            return (volume, effort)
        return (None, None)
    except Exception:
        # Catch all exceptions (syntax errors, parsing errors, etc.)
        return (None, None)


def dedent_snippet(code: str) -> str:
    """
    Normalize indentation by removing common leading whitespace.
    
    Similar to textwrap.dedent but handles edge cases gracefully.
    
    Args:
        code: Python source code string
    
    Returns:
        Code with normalized indentation
    """
    lines = code.splitlines()
    if not lines:
        return ""
    
    # Find minimum indentation (ignoring empty lines)
    indents = []
    for line in lines:
        if line.strip():  # Only consider non-empty lines
            indents.append(len(line) - len(line.lstrip()))
    
    if not indents:
        return code
    
    min_indent = min(indents)
    
    # Remove the minimum indentation from all lines
    dedented_lines = []
    for line in lines:
        if line.strip():  # Non-empty line
            dedented_lines.append(line[min_indent:] if len(line) >= min_indent else line.lstrip())
        else:  # Empty line
            dedented_lines.append("")
    
    return "\n".join(dedented_lines)


def _is_code_line(line: str) -> bool:
    """
    Check if a line contains actual code (not just comment or whitespace).
    
    Note: This does not handle multi-line strings used as comments.
    If future defects use multi-line strings as comments in function bodies,
    this function would need to be extended with state tracking.
    
    Args:
        line: The line to check
    
    Returns:
        True if line contains code, False if it's empty/whitespace/comment-only
    """
    stripped = line.strip()
    if not stripped:
        return False  # Empty or whitespace-only
    if stripped.startswith('#'):
        return False  # Comment-only line
    return True


def get_expected_changed_lines(defect_id: str) -> set:
    """
    Compare buggy function (from source file) with GT fix to find which source lines differ.
    
    Uses AST to locate the function in the source file and maps differences back to
    source-file-absolute line numbers for accurate slice coverage calculation.
    
    Args:
        defect_id: Defect identifier (e.g., 'defect1_py')
    
    Returns:
        Set of SOURCE-FILE-ABSOLUTE line numbers (1-indexed) that differ between buggy and GT fix.
        Returns empty set if defect not found or comparison fails.
    """
    # Find defect in python_defects
    defect = next((d for d in python_defects if d["id"] == defect_id), None)
    if defect is None:
        return set()
    
    source_path = defect["source_path"]
    function_name = defect.get("function_name")
    
    if not function_name or not os.path.exists(source_path):
        return set()
    
    # Get GT fix path
    defect_num = defect_id.replace('_py', '')
    gt_path = os.path.join(MINIMAL_FIX_DIR, f"{defect_num}_fix_raw.py")
    
    if not os.path.exists(gt_path):
        return set()
    
    try:
        # Read source file and extract function with line mapping
        with open(source_path, "r") as f:
            source_code = f.read()
        
        extracted = _extract_function_with_line_mapping(source_code, function_name)
        if not extracted:
            return set()
        
        # Read GT fix
        with open(gt_path, "r") as f:
            gt_code = f.read()
        gt_lines = gt_code.splitlines()
        
        # Extract just the code from our mapping
        buggy_lines_raw = [code for (_, code) in extracted]
        
        # Normalize indentation: dedent both to remove class-level indentation
        # Find minimum indentation in buggy code (ignoring empty lines)
        buggy_indents = [len(line) - len(line.lstrip()) for line in buggy_lines_raw if line.strip()]
        buggy_base_indent = min(buggy_indents) if buggy_indents else 0
        
        gt_indents = [len(line) - len(line.lstrip()) for line in gt_lines if line.strip()]
        gt_base_indent = min(gt_indents) if gt_indents else 0
        
        # Dedent both to normalize
        def dedent_line(line, indent):
            if not line.strip():
                return ""
            return line[indent:] if len(line) >= indent else line.lstrip()
        
        buggy_lines_norm = [dedent_line(line, buggy_base_indent).rstrip() for line in buggy_lines_raw]
        gt_lines_norm = [dedent_line(line, gt_base_indent).rstrip() for line in gt_lines]
        
        # Use difflib to find which buggy lines are modified/deleted
        matcher = SequenceMatcher(None, buggy_lines_norm, gt_lines_norm)
        
        changed_source_lines = set()
        
        for op, i1, i2, j1, j2 in matcher.get_opcodes():
            if op == 'equal':
                # Lines match, no change needed
                continue
            elif op == 'replace':
                # Lines i1:i2 in buggy are replaced by j1:j2 in GT
                for i in range(i1, i2):
                    changed_source_lines.add(extracted[i][0])
            elif op == 'delete':
                # Lines i1:i2 in buggy are deleted in GT
                for i in range(i1, i2):
                    changed_source_lines.add(extracted[i][0])
            elif op == 'insert':
                # Lines j1:j2 are inserted in GT (not in buggy)
                # Mark the insertion point - the line before where insertion happens
                if i1 > 0:
                    changed_source_lines.add(extracted[i1 - 1][0])
                elif extracted:
                    # Insertion at the very beginning - mark first line
                    changed_source_lines.add(extracted[0][0])
        
        # Filter out non-code lines (comments, blank lines)
        # These often differ between source and GT fix files but aren't actual bug fixes
        filtered_changed_lines = set()
        for src_line_num in changed_source_lines:
            # Find the original source line content from extracted
            for (line_num, code) in extracted:
                if line_num == src_line_num:
                    if _is_code_line(code):
                        filtered_changed_lines.add(src_line_num)
                    break
        
        return filtered_changed_lines
        
    except Exception as e:
        print(f"Error computing expected changed lines for {defect_id}: {e}")
        return set()


def get_actual_changed_lines(defect_id: str, raw_fix_path: str) -> set:
    """
    Compare buggy function (from source file) with LLM-generated fix to find which source lines differ.
    
    Similar to get_expected_changed_lines() but compares against the generated fix
    instead of the ground truth fix.
    
    Args:
        defect_id: Defect identifier (e.g., 'defect1_py')
        raw_fix_path: Path to the generated fix file (*_raw.py)
    
    Returns:
        Set of SOURCE-FILE-ABSOLUTE line numbers (1-indexed) that differ between buggy and generated fix.
        Returns empty set if defect not found or comparison fails.
    """
    # Find defect in python_defects
    defect = next((d for d in python_defects if d["id"] == defect_id), None)
    if defect is None:
        return set()
    
    source_path = defect["source_path"]
    function_name = defect.get("function_name")
    
    if not function_name or not os.path.exists(source_path):
        return set()
    
    if not os.path.exists(raw_fix_path):
        return set()
    
    try:
        # Read source file and extract function with line mapping
        with open(source_path, "r") as f:
            source_code = f.read()
        
        extracted = _extract_function_with_line_mapping(source_code, function_name)
        if not extracted:
            return set()
        
        # Read generated fix
        with open(raw_fix_path, "r") as f:
            fix_code = f.read()
        fix_lines = fix_code.splitlines()
        
        # Extract just the code from our mapping
        buggy_lines_raw = [code for (_, code) in extracted]
        
        # Normalize indentation: dedent both to remove class-level indentation
        buggy_indents = [len(line) - len(line.lstrip()) for line in buggy_lines_raw if line.strip()]
        buggy_base_indent = min(buggy_indents) if buggy_indents else 0
        
        fix_indents = [len(line) - len(line.lstrip()) for line in fix_lines if line.strip()]
        fix_base_indent = min(fix_indents) if fix_indents else 0
        
        # Dedent both to normalize
        def dedent_line(line, indent):
            if not line.strip():
                return ""
            return line[indent:] if len(line) >= indent else line.lstrip()
        
        buggy_lines_norm = [dedent_line(line, buggy_base_indent).rstrip() for line in buggy_lines_raw]
        fix_lines_norm = [dedent_line(line, fix_base_indent).rstrip() for line in fix_lines]
        
        # Use difflib to find which buggy lines are modified/deleted
        matcher = SequenceMatcher(None, buggy_lines_norm, fix_lines_norm)
        
        changed_source_lines = set()
        
        for op, i1, i2, j1, j2 in matcher.get_opcodes():
            if op == 'equal':
                continue
            elif op == 'replace':
                for i in range(i1, i2):
                    changed_source_lines.add(extracted[i][0])
            elif op == 'delete':
                for i in range(i1, i2):
                    changed_source_lines.add(extracted[i][0])
            elif op == 'insert':
                if i1 > 0:
                    changed_source_lines.add(extracted[i1 - 1][0])
                elif extracted:
                    changed_source_lines.add(extracted[0][0])
        
        # Filter out non-code lines
        filtered_changed_lines = set()
        for src_line_num in changed_source_lines:
            for (line_num, code) in extracted:
                if line_num == src_line_num:
                    if _is_code_line(code):
                        filtered_changed_lines.add(src_line_num)
                    break
        
        return filtered_changed_lines
        
    except Exception as e:
        print(f"Error computing actual changed lines for {defect_id}: {e}")
        return set()


def compute_slice_coverage(expected_lines: set, actual_lines: set, slice_lines: set) -> dict:
    """
    Compute how many expected and actual fix lines are covered by the slice.
    
    Args:
        expected_lines: Set of source line numbers that SHOULD change (from GT comparison)
        actual_lines: Set of source line numbers that the LLM ACTUALLY changed
        slice_lines: Set of line numbers in the slice
    
    Returns:
        Dict with coverage metrics for both expected and actual lines
    """
    expected_covered = expected_lines & slice_lines
    actual_covered = actual_lines & slice_lines
    
    return {
        "expected_in_slice": len(expected_covered),
        "expected_total": len(expected_lines),
        "expected_coverage": len(expected_covered) / len(expected_lines) if expected_lines else 1.0,
        "actual_in_slice": len(actual_covered),
        "actual_total": len(actual_lines),
        "actual_coverage": len(actual_covered) / len(actual_lines) if actual_lines else 1.0,
    }


def detect_levels(results: list) -> list:
    """Extract unique context level names from results, preserving order of first appearance."""
    seen = set()
    levels = []
    for entry in results:
        level = entry.get("levels")
        if level and level not in seen:
            seen.add(level)
            levels.append(level)
    return levels



def load_results(language: str) -> list:
    """Load all results for a language."""
    results_path = os.path.join(RESULTS_DIR, language)
    if not os.path.exists(results_path):
        return []
    
    all_results = []
    for filename in os.listdir(results_path):
        if filename.startswith("results") and filename.endswith(".json"):
            with open(os.path.join(results_path, filename)) as f:
                all_results.extend(json.load(f))
    return all_results


def aggregate_scores(results: list, levels: list = None) -> dict:
    """Aggregate scores by context level."""
    if levels is None:
        levels = detect_levels(results)
    
    grouped = defaultdict(lambda: defaultdict(list))
    
    for entry in results:
        level = entry.get("levels", "unknown")
        scores = entry.get("scores")
        if scores is None:
            continue  # Skip entries without explanation scores (e.g., no-explanation baseline)
        for criterion in CRITERIA:
            if criterion in scores:
                grouped[level][criterion].append(scores[criterion])
    
    aggregated = {}
    for level in levels:
        aggregated[level] = {}
        for criterion in CRITERIA:
            values = grouped[level].get(criterion, [])
            if values:
                aggregated[level][criterion] = {
                    "mean": round(mean(values), 3),
                    "std": round(stdev(values), 3) if len(values) > 1 else 0.0,
                    "n": len(values)
                }
            else:
                aggregated[level][criterion] = {"mean": 0, "std": 0, "n": 0}
    
    return aggregated


def aggregate_by_defect(results: list, levels: list = None) -> dict:
    """Aggregate scores by defect and context level."""
    if levels is None:
        levels = detect_levels(results)
    
    grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    
    for entry in results:
        defect_id = entry.get("defect_id", "unknown")
        level = entry.get("levels", "unknown")
        scores = entry.get("scores")
        if scores is None:
            continue  # Skip entries without explanation scores (e.g., no-explanation baseline)
        for criterion in CRITERIA:
            if criterion in scores:
                grouped[defect_id][level][criterion].append(scores[criterion])
    
    aggregated = {}
    for defect_id in grouped:
        aggregated[defect_id] = {}
        for level in levels:
            aggregated[defect_id][level] = {}
            for criterion in CRITERIA:
                values = grouped[defect_id][level].get(criterion, [])
                if values:
                    aggregated[defect_id][level][criterion] = round(mean(values), 3)
                else:
                    aggregated[defect_id][level][criterion] = 0
    
    return aggregated


def aggregate_fix_results(results: list, levels: list = None, halstead_data: dict = None) -> dict:
    """Aggregate fix validation results by context level."""
    if levels is None:
        levels = detect_levels(results)
    
    grouped = defaultdict(lambda: {
        "passed": 0, "failed": 0, "total": 0, "minimal": 0, 
        "deviations": [], "jaccards": [], "levenshtein_distances": [],
        "expected_changed_lines": [], "actual_changed_lines": [],
        "slice_coverages": {
            "SLICE_BLOCK": {"expected": [], "actual": []}, 
            "SLICE_BACKWARD": {"expected": [], "actual": []}, 
            "SLICE_FORWARD": {"expected": [], "actual": []}, 
            "SLICE_UNION": {"expected": [], "actual": []}
        },
        "halstead": {
            "baseline_volume": [], "baseline_effort": [],
            "fix_volume": [], "fix_effort": [],
            "delta_volume": [], "delta_effort": []
        }
    })
    
    for entry in results:
        # Backward compatibility: check for 'validation' then 'verification'
        validation = entry.get("validation") or entry.get("verification", {})
        comparison = entry.get("comparison", {})
        level = entry.get("levels", "unknown")
        
        if validation:
            grouped[level]["total"] += 1
            if validation.get("passed", False):
                grouped[level]["passed"] += 1
                # Only track deviation, minimality, and jaccard for passing fixes
                if comparison:
                    if comparison.get("is_minimal_fix", False):
                        grouped[level]["minimal"] += 1
                    deviation = comparison.get("line_deviation")
                    if deviation is not None:
                        grouped[level]["deviations"].append(deviation)
                    jaccard = comparison.get("jaccard_similarity")
                    if jaccard is not None:
                        grouped[level]["jaccards"].append(jaccard)
                    lev = comparison.get("normalized_levenshtein")
                    if lev is not None:
                        grouped[level]["levenshtein_distances"].append(lev)
            else:
                grouped[level]["failed"] += 1
        
        # Track expected and actual changed lines for all entries (passed or failed)
        if comparison:
            expected_lines = comparison.get("expected_changed_lines", [])
            actual_lines = comparison.get("actual_changed_lines", [])
            if expected_lines:
                grouped[level]["expected_changed_lines"].append(len(expected_lines))
            if actual_lines:
                grouped[level]["actual_changed_lines"].append(len(actual_lines))
            
            # Track slice coverage metrics from comparison data
            slice_coverage = comparison.get("slice_coverage", {})
            if slice_coverage:
                for strategy_name, coverage_data in slice_coverage.items():
                    if strategy_name in grouped[level]["slice_coverages"]:
                        if coverage_data.get("expected_coverage") is not None:
                            grouped[level]["slice_coverages"][strategy_name]["expected"].append(
                                coverage_data["expected_coverage"]
                            )
                        if coverage_data.get("actual_coverage") is not None:
                            grouped[level]["slice_coverages"][strategy_name]["actual"].append(
                                coverage_data["actual_coverage"]
                            )
        
        # Collect Halstead metrics for this entry if available
        if halstead_data and "fixes" in halstead_data:
            defect_id = entry.get("defect_id")
            levels_str = entry.get("levels")
            run_id = entry.get("run_id", 1)
            
            if defect_id and levels_str:
                metrics = halstead_data["fixes"].get((defect_id, levels_str, run_id), {})
                
                # Append each metric if it's not None
                for metric_name in ["baseline_volume", "baseline_effort", "fix_volume", "fix_effort", "delta_volume", "delta_effort"]:
                    value = metrics.get(metric_name)
                    if value is not None:
                        grouped[level]["halstead"][metric_name].append(value)
    
    aggregated = {}
    for level in levels:
        data = grouped[level]
        total = data["total"]
        passed = data["passed"]
        deviations = data["deviations"]
        jaccards = data["jaccards"]
        levenshtein_dists = data["levenshtein_distances"]
        expected_counts = data["expected_changed_lines"]
        actual_counts = data["actual_changed_lines"]
        slice_coverages = data["slice_coverages"]
        
        level_data = {
            "passed": passed,
            "failed": data["failed"],
            "total": total,
            "rate": round(passed / total, 3) if total > 0 else 0.0,
            "minimal_rate": round(data["minimal"] / passed, 3) if passed > 0 else 0.0,
            "avg_deviation": round(mean(deviations), 2) if deviations else 0.0,
            "avg_jaccard": round(mean(jaccards), 3) if jaccards else 0.0,
            "avg_levenshtein": round(mean(levenshtein_dists), 3) if levenshtein_dists else 0.0,
            "avg_expected_changed_lines": round(mean(expected_counts), 2) if expected_counts else None,
            "avg_actual_changed_lines": round(mean(actual_counts), 2) if actual_counts else None,
        }
        
        # Slice coverage averages (only for levels that used slices)
        for strategy_key, csv_prefix in [
            ("SLICE_BLOCK", "block"), 
            ("SLICE_BACKWARD", "backward"), 
            ("SLICE_FORWARD", "forward"), 
            ("SLICE_UNION", "union")
        ]:
            expected_cov = slice_coverages[strategy_key]["expected"]
            actual_cov = slice_coverages[strategy_key]["actual"]
            level_data[f"{csv_prefix}_expected_coverage"] = round(mean(expected_cov), 3) if expected_cov else None
            level_data[f"{csv_prefix}_actual_coverage"] = round(mean(actual_cov), 3) if actual_cov else None
        
        # Halstead metrics aggregation (mean + std for baseline, fix, and delta)
        halstead = data["halstead"]
        for metric_name in ["baseline_volume", "baseline_effort", "fix_volume", "fix_effort", "delta_volume", "delta_effort"]:
            values = halstead[metric_name]
            if values:
                level_data[f"avg_{metric_name}"] = round(mean(values), 2)
                level_data[f"std_{metric_name}"] = round(stdev(values), 2) if len(values) > 1 else 0.0
            else:
                level_data[f"avg_{metric_name}"] = None
                level_data[f"std_{metric_name}"] = None
        
        aggregated[level] = level_data
    
    return aggregated


def save_fix_attempts_csv(halstead_data: dict, all_results: list, output_path: str):
    """
    Save per-attempt Halstead metrics to CSV.
    
    One row per (defect_id, level, run_id) attempt with all Halstead metrics.
    
    Args:
        halstead_data: Dict with "baseline" and "fixes" keys containing metrics
        all_results: List of result entries from JSON files
        output_path: Path to write CSV file
    """
    rows = []
    
    for entry in all_results:
        defect_id = entry.get("defect_id")
        levels = entry.get("levels")
        run_id = entry.get("run_id", 1)
        fix_file = entry.get("fix_file")
        
        if not defect_id or not fix_file:
            continue
        
        # Get passed status from validation or verification field
        validation = entry.get("validation") or entry.get("verification", {})
        passed = validation.get("passed", False) if validation else False
        
        # Look up metrics in halstead_data["fixes"] using the (defect_id, levels, run_id) tuple
        metrics = halstead_data["fixes"].get((defect_id, levels, run_id), {})
        
        row = {
            "Defect": defect_id,
            "Level": levels,
            "Run": run_id,
            "Passed": 1 if passed else 0,
            "Baseline_Volume": metrics.get("baseline_volume"),
            "Baseline_Effort": metrics.get("baseline_effort"),
            "Fix_Volume": metrics.get("fix_volume"),
            "Fix_Effort": metrics.get("fix_effort"),
            "Delta_Volume": metrics.get("delta_volume"),
            "Delta_Effort": metrics.get("delta_effort"),
        }
        rows.append(row)
    
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"Saved: {output_path}")


def save_fix_csv(fix_agg: dict, output_path: str):
    """Save fix validation results as CSV."""
    rows = []
    for level, data in fix_agg.items():
        row = {
            "Level": level,
            "Passed": data["passed"],
            "Failed": data["failed"],
            "Total": data["total"],
            "Pass_Rate": data["rate"],
            "Minimal_Fix_Rate": data["minimal_rate"],
            "Avg_Line_Deviation": data["avg_deviation"],
            "Avg_Jaccard_Similarity": data["avg_jaccard"],
            "Avg_Normalized_Levenshtein": data["avg_levenshtein"],
        }
        
        # Add expected/actual changed lines (if data exists)
        if data.get("avg_expected_changed_lines") is not None:
            row["Avg_Expected_Changed_Lines"] = data["avg_expected_changed_lines"]
        if data.get("avg_actual_changed_lines") is not None:
            row["Avg_Actual_Changed_Lines"] = data["avg_actual_changed_lines"]
        
        # Add slice coverage columns (only if data exists for this level)
        # Expected coverage
        if data.get("block_expected_coverage") is not None:
            row["Block_Expected_Coverage"] = data["block_expected_coverage"]
        if data.get("backward_expected_coverage") is not None:
            row["Backward_Expected_Coverage"] = data["backward_expected_coverage"]
        if data.get("forward_expected_coverage") is not None:
            row["Forward_Expected_Coverage"] = data["forward_expected_coverage"]
        if data.get("union_expected_coverage") is not None:
            row["Union_Expected_Coverage"] = data["union_expected_coverage"]
        
        # Actual coverage
        if data.get("block_actual_coverage") is not None:
            row["Block_Actual_Coverage"] = data["block_actual_coverage"]
        if data.get("backward_actual_coverage") is not None:
            row["Backward_Actual_Coverage"] = data["backward_actual_coverage"]
        if data.get("forward_actual_coverage") is not None:
            row["Forward_Actual_Coverage"] = data["forward_actual_coverage"]
        if data.get("union_actual_coverage") is not None:
            row["Union_Actual_Coverage"] = data["union_actual_coverage"]
        
        # Add Halstead metrics (aggregated: avg and std for baseline, fix, delta)
        for metric_name in ["baseline_volume", "baseline_effort", "fix_volume", "fix_effort", "delta_volume", "delta_effort"]:
            avg_key = f"avg_{metric_name}"
            std_key = f"std_{metric_name}"
            
            if data.get(avg_key) is not None:
                # Convert metric_name to proper CSV column name (e.g., baseline_volume -> Avg_Baseline_Volume)
                parts = metric_name.split("_")
                col_name = "Avg_" + "_".join(p.capitalize() for p in parts)
                row[col_name] = data[avg_key]
            
            if data.get(std_key) is not None:
                # Convert metric_name to proper CSV column name (e.g., baseline_volume -> Std_Baseline_Volume)
                parts = metric_name.split("_")
                col_name = "Std_" + "_".join(p.capitalize() for p in parts)
                row[col_name] = data[std_key]
        
        rows.append(row)
    
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"Saved: {output_path}")


def plot_fix_success_rates(fix_agg: dict, output_dir: str):
    """Bar chart of fix pass rates with line deviation overlay."""
    levels = list(fix_agg.keys())
    rates = [fix_agg[l]["rate"] for l in levels]
    deviations = [fix_agg[l]["avg_deviation"] for l in levels]
    
    fig, ax1 = plt.subplots(figsize=(max(10, len(levels) * 0.6), 6))
    
    # Primary axis: Pass Rate
    colors = ["#27ae60" if r >= 0.5 else "#e74c3c" for r in rates]
    x = range(len(levels))
    bars = ax1.bar(x, rates, color=colors, edgecolor='black', linewidth=0.5, alpha=0.7, label="Pass Rate")
    
    # Add count labels on bars
    for i, (bar, level) in enumerate(zip(bars, levels)):
        data = fix_agg[level]
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f"{data['passed']}/{data['total']}", ha='center', va='bottom', fontsize=8)
    
    ax1.set_xlabel("Context Level")
    ax1.set_ylabel("Fix Pass Rate")
    ax1.set_ylim(0, 1.15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(levels, rotation=45, ha='right')
    ax1.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
    ax1.grid(axis="y", alpha=0.3)
    
    # Secondary axis: Avg Line Deviation
    ax2 = ax1.twinx()
    ax2.plot(x, deviations, color="#2980b9", marker='o', linestyle='-', linewidth=2, label="Avg Line Deviation")
    ax2.set_ylabel("Avg Line Deviation (Added + Removed Lines)")
    # Set limit based on max deviation with some padding
    max_dev = max(deviations) if deviations else 0
    ax2.set_ylim(0, max_dev * 1.2 if max_dev > 0 else 10)
    
    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.title("Fix Validation Success Rate & Efficiency", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fix_success_rates.png"), dpi=150)
    plt.close()
    print(f"Saved: fix_success_rates.png")


def plot_fix_quality_metrics(fix_agg: dict, output_dir: str):
    """Bar chart of fix quality metrics: Line Deviation, Jaccard Similarity, and Normalized Levenshtein."""
    levels = list(fix_agg.keys())
    deviations = [fix_agg[l]["avg_deviation"] for l in levels]
    jaccards = [fix_agg[l]["avg_jaccard"] for l in levels]
    levenshtein = [fix_agg[l]["avg_levenshtein"] for l in levels]
    
    fig, ax1 = plt.subplots(figsize=(max(10, len(levels) * 0.6), 6))
    
    x = range(len(levels))
    
    # Primary axis: Line Deviation (bars)
    colors = ["#3498db" if d <= 10 else "#e67e22" if d <= 20 else "#e74c3c" for d in deviations]
    bars = ax1.bar(x, deviations, color=colors, edgecolor='black', linewidth=0.5, alpha=0.7, label="Avg Line Deviation")
    
    ax1.set_xlabel("Context Level")
    ax1.set_ylabel("Avg Line Deviation (Added + Removed Lines)", color="#2980b9")
    ax1.set_xticks(x)
    ax1.set_xticklabels(levels, rotation=45, ha='right')
    ax1.tick_params(axis='y', labelcolor="#2980b9")
    ax1.grid(axis="y", alpha=0.3)
    
    # Secondary axis: Similarity metrics (lines)
    ax2 = ax1.twinx()
    ax2.plot(x, jaccards, color="#27ae60", marker='s', linestyle='-', linewidth=2, markersize=6, label="Avg Jaccard Similarity")
    ax2.plot(x, levenshtein, color="#8e44ad", marker='^', linestyle='--', linewidth=2, markersize=6, label="Avg Norm. Levenshtein Dist.")
    ax2.set_ylabel("Similarity / Distance (0-1)")
    ax2.set_ylim(0, 1.05)
    ax2.axhline(y=0.5, color='gray', linestyle='--', alpha=0.3)
    
    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    plt.title("Fix Quality: Line Deviation, Jaccard Similarity & Levenshtein Distance", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fix_quality_metrics.png"), dpi=150)
    plt.close()
    print(f"Saved: fix_quality_metrics.png")


def plot_changed_lines_comparison(fix_agg: dict, output_dir: str):
    """Grouped bar chart comparing expected vs actual changed lines."""
    # Filter levels that have expected/actual changed lines data
    levels_with_data = []
    expected_lines = []
    actual_lines = []
    
    for level in fix_agg.keys():
        exp = fix_agg[level].get("avg_expected_changed_lines")
        act = fix_agg[level].get("avg_actual_changed_lines")
        if exp is not None and act is not None:
            levels_with_data.append(level)
            expected_lines.append(exp)
            actual_lines.append(act)
    
    if not levels_with_data:
        print("No expected/actual changed lines data found, skipping plot")
        return
    
    fig, ax = plt.subplots(figsize=(max(12, len(levels_with_data) * 0.7), 6))
    
    x = range(len(levels_with_data))
    width = 0.35
    
    # Grouped bars
    bars1 = ax.bar([i - width/2 for i in x], expected_lines, width, 
                   label="Expected Changed Lines", color="#3498db", edgecolor='black', linewidth=0.5, alpha=0.8)
    bars2 = ax.bar([i + width/2 for i in x], actual_lines, width,
                   label="Actual Changed Lines", color="#e67e22", edgecolor='black', linewidth=0.5, alpha=0.8)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.1,
                   f'{height:.1f}', ha='center', va='bottom', fontsize=7)
    
    ax.set_xlabel("Context Level")
    ax.set_ylabel("Average Number of Changed Lines")
    ax.set_xticks(x)
    ax.set_xticklabels(levels_with_data, rotation=45, ha='right')
    ax.legend(loc='upper right')
    ax.grid(axis="y", alpha=0.3)
    
    # Add reference line at y=1 (minimal fix)
    ax.axhline(y=1, color='green', linestyle='--', alpha=0.5, label='Minimal Fix (1 line)')
    
    plt.title("Expected vs Actual Changed Lines by Context Level", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "changed_lines_comparison.png"), dpi=150)
    plt.close()
    print(f"Saved: changed_lines_comparison.png")


def save_csv(python_agg: dict, output_path: str):
    """Save aggregated results as CSV."""
    levels = list(python_agg.keys())
    rows = []
    for level in levels:
        for criterion in CRITERIA:
            p = python_agg.get(level, {}).get(criterion, {"mean": 0, "std": 0})
            rows.append({
                "Levels": level,
                "Criterion": criterion,
                "Mean": p["mean"] if isinstance(p, dict) else 0,
                "Std": p["std"] if isinstance(p, dict) else 0
            })
    
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"Saved: {output_path}")


def save_defect_csv(python_by_defect: dict, output_path: str):
    """Save per-defect results as CSV."""
    rows = []
    
    for defect_id, level_data in python_by_defect.items():
        for level in level_data.keys():
            row = {"Defect": defect_id, "Levels": level}
            for criterion in CRITERIA:
                row[criterion] = level_data.get(level, {}).get(criterion, 0)
            rows.append(row)
    
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"Saved: {output_path}")


def plot_comparison_bars(python_agg: dict, output_dir: str):
    """Generate bar charts per criterion with dynamic width adjustment."""
    os.makedirs(output_dir, exist_ok=True)
    levels = list(python_agg.keys())
    
    if not levels:
        print("No levels found, skipping comparison bars")
        return
    
    for criterion in CRITERIA:
        fig_width = max(10, len(levels) * 0.5)
        fig, ax = plt.subplots(figsize=(fig_width, 5))
        
        x = range(len(levels))
        width = 0.7
        
        python_means = [python_agg.get(s, {}).get(criterion, {}).get("mean", 0) for s in levels]
        python_stds = [python_agg.get(s, {}).get(criterion, {}).get("std", 0) for s in levels]
        ax.bar(x, python_means, width, yerr=python_stds, color="#e74c3c", capsize=3)
        
        ax.set_xlabel("Context Level")
        ax.set_ylabel("Score")
        ax.set_title(f"{criterion}")
        ax.set_xticks(x)
        ax.set_xticklabels(levels, rotation=45, ha='right')
        ax.set_ylim(0, 1.1)
        ax.grid(axis="y", alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{criterion}.png"), dpi=150)
        plt.close()
    
    print(f"Saved: {len(CRITERIA)} criterion comparison charts")


def plot_heatmaps(python_agg: dict, output_dir: str):
    """Generate heatmap for Python results with dynamic width adjustment."""
    levels = list(python_agg.keys())
    
    if not levels:
        print("No levels found, skipping heatmap")
        return
    
    data = []
    for criterion in CRITERIA:
        row = [python_agg[level][criterion]["mean"] for level in levels]
        data.append(row)
    
    df = pd.DataFrame(data, index=CRITERIA, columns=levels)
    avg_row = df.mean(axis=0)
    df.loc["AVERAGE"] = avg_row
    
    # Dynamic figure width based on number of columns
    fig_width = max(10, len(levels) * 0.8)
    fig, ax = plt.subplots(figsize=(fig_width, 7))
    sns.heatmap(df, annot=True, fmt=".2f", cmap="YlGnBu", vmin=0, vmax=1, ax=ax)
    ax.set_title("Python Scores by Context Level")
    ax.set_xlabel("Context Level")
    ax.set_ylabel("Criterion")
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "heatmap.png"), dpi=150)
    plt.close()
    print(f"Saved: heatmap.png")


def plot_defect_charts(python_by_defect: dict, output_dir: str):
    """Generate per-defect bar charts showing all criteria across levels."""
    defects_dir = os.path.join(output_dir, "defects")
    os.makedirs(defects_dir, exist_ok=True)
    
    # Detect levels from first available defect
    levels = []
    for defect_data in python_by_defect.values():
        if defect_data:
            levels = list(defect_data.keys())
            break
    
    defect_ids = sorted(python_by_defect.keys())
    
    for defect_id in defect_ids:
        python_data = python_by_defect.get(defect_id, {})
        
        if not python_data:
            continue
        
        fig, axes = plt.subplots(2, 3, figsize=(14, 8))
        axes = axes.flatten()
        
        for idx, criterion in enumerate(CRITERIA):
            ax = axes[idx]
            
            x = range(len(levels))
            width = 0.7
            
            python_vals = [python_data.get(s, {}).get(criterion, 0) for s in levels]
            
            ax.bar(x, python_vals, width, label="Python", color="#e74c3c")
            
            ax.set_title(criterion.replace("_", " "), fontsize=10)
            ax.set_xticks(x)
            ax.set_xticklabels([s[:8] for s in levels], rotation=45, fontsize=8)
            ax.legend(fontsize=8)
            ax.grid(axis="y", alpha=0.3)
        
        fig.suptitle(f"Defect: {defect_id}", fontsize=14, fontweight="bold")
        plt.tight_layout()
        plt.savefig(os.path.join(defects_dir, f"{defect_id}.png"), dpi=150)
        plt.close()
    
    print(f"Saved: {len(defect_ids)} defect charts to {defects_dir}/")





def plot_run_variance(results: list, output_dir: str):
    """Strategy D: Per-run success rates to assess LLM consistency."""
    runs = sorted(set(entry.get("run_id", 1) for entry in results))
    
    if len(runs) <= 1:
        print("Skipping run variance: only 1 run found")
        return
    
    def success_rate(scores):
        return sum(scores) / len(scores) if scores else 0
    
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    axes = axes.flatten()
    
    for idx, criterion in enumerate(CRITERIA):
        ax = axes[idx]
        
        rates = []
        for run_id in runs:
            scores = [entry["scores"].get(criterion, 0) 
                     for entry in results 
                     if entry.get("run_id") == run_id and entry.get("scores") is not None]
            rates.append(success_rate(scores))
        
        colors = plt.cm.Paired(range(len(runs)))
        x = range(len(runs))
        ax.bar(x, rates, color=colors, edgecolor='black', linewidth=0.5)
        
        # Add variance annotation
        if len(rates) > 1:
            variance = stdev(rates)
            ax.text(0.95, 0.95, f'σ = {variance:.3f}', transform=ax.transAxes,
                   ha='right', va='top', fontsize=9, 
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax.set_title(criterion.replace('_', ' '), fontsize=10, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([f"Run {r}" for r in runs], fontsize=8)
        ax.set_ylim(0, 1.1)
        ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.4)
        ax.grid(axis="y", alpha=0.3)
    
    fig.suptitle("Run-to-Run Variance: LLM Evaluation Consistency", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "run_variance.png"), dpi=150)
    plt.close()
    
    print(f"Saved: run_variance.png")


def jaccard_similarity(code_a: str, code_b: str) -> float:
    """
    Compute Jaccard similarity between two normalized code strings.
    Each non-empty line (stripped) is treated as a set element.
    
    Returns:
        Float between 0.0 (completely different) and 1.0 (identical)
    """
    lines_a = set(line.strip() for line in code_a.splitlines() if line.strip())
    lines_b = set(line.strip() for line in code_b.splitlines() if line.strip())
    
    if not lines_a and not lines_b:
        return 1.0  # Both empty = identical
    
    intersection = lines_a & lines_b
    union = lines_a | lines_b
    
    return len(intersection) / len(union) if union else 1.0


def normalized_levenshtein(code_a: str, code_b: str) -> float:
    """
    Compute normalized Levenshtein distance between two normalized code strings.
    Each non-empty line (stripped) is treated as a sequence element,
    matching the same granularity as jaccard_similarity.
    
    Uses difflib.SequenceMatcher to approximate edit distance at line level.
    
    Returns:
        Float between 0.0 (identical) and 1.0 (completely different)
    """
    lines_a = [line.strip() for line in code_a.splitlines() if line.strip()]
    lines_b = [line.strip() for line in code_b.splitlines() if line.strip()]
    
    if not lines_a and not lines_b:
        return 0.0  # Both empty = identical
    
    matcher = SequenceMatcher(None, lines_a, lines_b)
    return round(1.0 - matcher.ratio(), 6)


def compute_baseline_metrics() -> dict:
    """
    Compute baseline Halstead metrics for all defects.
    
    Extracts the buggy function from each defect's source file,
    computes Halstead volume and effort, and caches them in a dictionary.
    
    Returns:
        Dict mapping defect_id -> {"volume": float|None, "effort": float|None}
    """
    baseline_cache = {}
    
    for defect in python_defects:
        defect_id = defect["id"]
        source_path = defect["source_path"]
        function_name = defect.get("function_name")
        
        if not function_name or not os.path.exists(source_path):
            baseline_cache[defect_id] = {"volume": None, "effort": None}
            continue
        
        try:
            # Read source file and extract function with line mapping
            with open(source_path, "r") as f:
                source_code = f.read()
            
            extracted = _extract_function_with_line_mapping(source_code, function_name)
            if not extracted:
                baseline_cache[defect_id] = {"volume": None, "effort": None}
                continue
            
            # Extract just the code lines (ignoring line numbers)
            code_lines = [code for (_, code) in extracted]
            buggy_code = "\n".join(code_lines)
            
            # Dedent before computing Halstead
            dedented_code = dedent_snippet(buggy_code)
            
            # Compute Halstead metrics
            volume, effort = compute_halstead_volume_effort(dedented_code)
            baseline_cache[defect_id] = {"volume": volume, "effort": effort}
            
        except Exception as e:
            print(f"Error computing baseline metrics for {defect_id}: {e}")
            baseline_cache[defect_id] = {"volume": None, "effort": None}
    
    return baseline_cache


def compute_fix_metrics_for_results(all_results: list, baseline_cache: dict, results_dir: str) -> dict:
    """
    Compute Halstead metrics for all fix attempts and delta from baseline.
    
    Args:
        all_results: List of result entries from JSON files
        baseline_cache: Dict mapping defect_id -> baseline metrics
        results_dir: Path to directory containing fix files
    
    Returns:
        Dict mapping (defect_id, levels, run_id) -> {
            "baseline_volume": float|None,
            "baseline_effort": float|None,
            "fix_volume": float|None,
            "fix_effort": float|None,
            "delta_volume": float|None,
            "delta_effort": float|None
        }
    """
    metrics_cache = {}
    
    for entry in all_results:
        defect_id = entry.get("defect_id")
        levels = entry.get("levels")
        run_id = entry.get("run_id", 1)
        fix_file = entry.get("fix_file")
        
        if not defect_id or not fix_file:
            continue
        
        # Get baseline metrics
        baseline = baseline_cache.get(defect_id, {})
        baseline_volume = baseline.get("volume")
        baseline_effort = baseline.get("effort")
        
        # Derive raw fix path
        raw_fix_name = fix_file.replace(".py", "_raw.py")
        raw_fix_path = os.path.join(results_dir, raw_fix_name)
        
        if not os.path.exists(raw_fix_path):
            metrics_cache[(defect_id, levels, run_id)] = {
                "baseline_volume": baseline_volume,
                "baseline_effort": baseline_effort,
                "fix_volume": None,
                "fix_effort": None,
                "delta_volume": None,
                "delta_effort": None
            }
            continue
        
        try:
            # Read fix file
            with open(raw_fix_path, "r") as f:
                fix_code = f.read()
            
            # Dedent before computing Halstead
            dedented_fix = dedent_snippet(fix_code)
            
            # Compute Halstead metrics for fix
            fix_volume, fix_effort = compute_halstead_volume_effort(dedented_fix)
            
            # Compute deltas (after - before)
            delta_volume = None
            delta_effort = None
            
            if fix_volume is not None and baseline_volume is not None:
                delta_volume = fix_volume - baseline_volume
            
            if fix_effort is not None and baseline_effort is not None:
                delta_effort = fix_effort - baseline_effort
            
            metrics_cache[(defect_id, levels, run_id)] = {
                "baseline_volume": baseline_volume,
                "baseline_effort": baseline_effort,
                "fix_volume": fix_volume,
                "fix_effort": fix_effort,
                "delta_volume": delta_volume,
                "delta_effort": delta_effort
            }
            
        except Exception as e:
            print(f"Error computing fix metrics for {defect_id} {levels} run{run_id}: {e}")
            metrics_cache[(defect_id, levels, run_id)] = {
                "baseline_volume": baseline_volume,
                "baseline_effort": baseline_effort,
                "fix_volume": None,
                "fix_effort": None,
                "delta_volume": None,
                "delta_effort": None
            }
    
    return metrics_cache


def compare_with_ground_truth(defect_id, results_dir, fix_file, slice_lines_info=None):
    """Compare a generated fix with the ground truth minimal fix.
    
    Args:
        defect_id: Defect identifier (e.g., 'defect1_py')
        results_dir: Directory containing the fix files
        fix_file: Name of the fix file (e.g., 'defect1_py_CODE_ERROR_run1_fix.py')
        slice_lines_info: Optional dict mapping slice strategy names to line number lists
                          e.g., {'SLICE_BLOCK': [10, 11, 12], 'SLICE_BACKWARD': [8, 10, 11]}
    
    Returns:
        Dict with comparison results, or None if comparison fails:
        {
            'is_minimal_fix': bool,
            'diff_to_ground_truth': str,
            'line_deviation': int,
            'jaccard_similarity': float,
            'expected_changed_lines': list[int],
            'actual_changed_lines': list[int],
            'slice_coverage': {
                'SLICE_BLOCK': {'expected_coverage': float, 'actual_coverage': float, ...},
                ...
            } or None
        }
    """
    if not fix_file:
        return None
    
    # Derive raw fix path
    raw_fix_name = fix_file.replace(".py", "_raw.py")
    raw_fix_path = os.path.join(results_dir, raw_fix_name)
    
    # Ground truth path
    gt_name = f"{defect_id}_fix_raw.py"
    gt_path = os.path.join(MINIMAL_FIX_DIR, gt_name)
    if not os.path.exists(gt_path):
        gt_path = os.path.join(MINIMAL_FIX_DIR, f"{defect_id.replace('_py', '')}_fix_raw.py")
    
    if not os.path.exists(gt_path) or not os.path.exists(raw_fix_path):
        return None
    
    try:
        with open(gt_path, "r") as f:
            gt_code = f.read()
        with open(raw_fix_path, "r") as f:
            raw_code = f.read()
            
        # Normalize both
        gt_norm = normalize_python_code(gt_code)
        raw_norm = normalize_python_code(raw_code)
        
        is_minimal = (gt_norm == raw_norm)
        
        # Generate unified diff of normalized versions
        diff_lines = list(unified_diff(
            gt_norm.splitlines(),
            raw_norm.splitlines(),
            fromfile=f"ground_truth/{defect_id}",
            tofile=f"generated_fix/{fix_file}",
            lineterm=""
        ))
        diff_output = "\n".join(diff_lines)
        
        # Calculate line deviation (added + removed lines in normalized code)
        deviation = 0
        if diff_lines:
            for line in diff_lines:
                if (line.startswith("+") or line.startswith("-")) and not (line.startswith("+++") or line.startswith("---")):
                    deviation += 1
        
        # Calculate Jaccard similarity
        jaccard = jaccard_similarity(gt_norm, raw_norm)
        
        # Calculate normalized Levenshtein distance
        levenshtein = normalized_levenshtein(gt_norm, raw_norm)
        
        # Get expected and actual changed lines (source-file line numbers)
        expected_lines = get_expected_changed_lines(defect_id)
        actual_lines = get_actual_changed_lines(defect_id, raw_fix_path)
        
        # Compute slice coverage for each slice strategy if provided
        slice_coverage = None
        if slice_lines_info:
            slice_coverage = {}
            for strategy_name, lines in slice_lines_info.items():
                if lines is not None:
                    slice_set = set(lines)
                    coverage = compute_slice_coverage(expected_lines, actual_lines, slice_set)
                    slice_coverage[strategy_name] = coverage
        
        return {
            "is_minimal_fix": is_minimal,
            "diff_to_ground_truth": diff_output,
            "line_deviation": deviation,
            "jaccard_similarity": jaccard,
            "normalized_levenshtein": levenshtein,
            "expected_changed_lines": sorted(list(expected_lines)),
            "actual_changed_lines": sorted(list(actual_lines)),
            "slice_coverage": slice_coverage
        }
    except Exception as e:
        print(f"Comparison error for {fix_file}: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Generate comparison report")
    parser.add_argument("--save-plots", action="store_true", help="Save all plots")
    parser.add_argument("--save-csv", action="store_true", help="Save CSV files")
    parser.add_argument("--results-dir", type=str, default=None, help="Custom results directory (e.g., results/29_12)")
    parser.add_argument("--no-compare-gt", action="store_true", help="Skip comparing fixes with ground truth (comparison is enabled by default)")
    args = parser.parse_args()
    
    # Use custom results dir if specified
    results_dir = args.results_dir if args.results_dir else RESULTS_DIR
    
    # Load results from python subfolder
    python_path = os.path.join(results_dir, "python") if "python" not in results_dir else results_dir
    if not os.path.exists(python_path):
        print(f"No results found in {python_path}")
        return
    
    all_results = []
    files_to_update = {}
    
    for filename in os.listdir(python_path):
        if filename.startswith("results") and filename.endswith(".json"):
            file_path = os.path.join(python_path, filename)
            with open(file_path) as f:
                data = json.load(f)
                all_results.extend(data)
                if not args.no_compare_gt:
                    files_to_update[file_path] = data
    
    if not args.no_compare_gt:
        modified_files = set()
        print("Comparing fixes with ground truth...")
        for entry in all_results:
            defect_id = entry.get("defect_id")
            fix_file = entry.get("fix_file")
            slice_lines_info = entry.get("slice_lines", {})
            
            # Compare all entries (passed or failed) to get expected/actual changed lines
            if defect_id and fix_file:
                comparison_result = compare_with_ground_truth(
                    defect_id, python_path, fix_file, slice_lines_info
                )
                if comparison_result is not None:
                    # Check if 'comparison' already exists and if it's the same
                    if entry.get("comparison") != comparison_result:
                        entry["comparison"] = comparison_result
                        # Find which file this entry belongs to and mark as modified
                        for file_path, file_data in files_to_update.items():
                            if entry in file_data:
                                modified_files.add(file_path)
        
        # Save updated JSON files
        for file_path in modified_files:
            with open(file_path, "w") as f:
                json.dump(files_to_update[file_path], f, indent=2)
            print(f"Updated: {file_path}")
    
    if not all_results:
        print(f"No results found in {python_path}")
        return
    
    print(f"Loaded: {len(all_results)} Python entries from {python_path}")
    
    # Compute Halstead metrics for baselines and fixes
    print("Computing baseline Halstead metrics...")
    baseline_metrics = compute_baseline_metrics()
    
    print("Computing Halstead metrics for all fix attempts...")
    fix_metrics = compute_fix_metrics_for_results(all_results, baseline_metrics, python_path)
    
    # Store metrics in a runtime data structure accessible for later use
    # Note: We don't persist this to JSON files, it's just for in-memory analysis
    halstead_data = {
        "baseline": baseline_metrics,
        "fixes": fix_metrics
    }
    
    print(f"Computed Halstead metrics for {len(baseline_metrics)} defects and {len(fix_metrics)} fix attempts")
    
    # Aggregate
    python_agg = aggregate_scores(all_results)
    python_by_defect = aggregate_by_defect(all_results)
    fix_agg = aggregate_fix_results(all_results, halstead_data=halstead_data)
    
    reports_dir = resolve_reports_dir(python_path)
    os.makedirs(reports_dir, exist_ok=True)
    
    if args.save_csv:
        save_csv(python_agg, os.path.join(reports_dir, "comparison.csv"))
        save_defect_csv(python_by_defect, os.path.join(reports_dir, "defect_breakdown.csv"))
        save_fix_attempts_csv(halstead_data, all_results, os.path.join(reports_dir, "fix_attempts.csv"))
        save_fix_csv(fix_agg, os.path.join(reports_dir, "fix_results.csv"))
    
    if args.save_plots:
        plot_comparison_bars(python_agg, reports_dir)
        plot_heatmaps(python_agg, reports_dir)
        plot_defect_charts(python_by_defect, reports_dir)
        plot_fix_success_rates(fix_agg, reports_dir)
        plot_run_variance(all_results, reports_dir)
    
    print(f"\n✓ All reports saved to {reports_dir}/")
    
    try:
        run_count = len(set(entry.get("run_id") for entry in all_results if entry.get("run_id")))
        has_explanations_flag = any(entry.get("scores") is not None for entry in all_results)
        
        if run_count >= 2:
            metrics_result = run_explanation_metrics(
                results_dir=python_path,
                reports_dir=reports_dir,
                has_explanations=has_explanations_flag,
                min_runs=2
            )
            if metrics_result["status"] == "ran":
                print(f"✓ Explanation metrics: {metrics_result['message']}")
            elif metrics_result["status"] == "skipped":
                print(f"⊘ Explanation metrics: {metrics_result['message']}")
            else:
                print(f"⚠ Warning: Explanation metrics failed: {metrics_result['message']}")
    except Exception as e:
        print(f"⚠ Warning: Explanation metrics wrapper failed: {str(e)}")



if __name__ == "__main__":
    main()
