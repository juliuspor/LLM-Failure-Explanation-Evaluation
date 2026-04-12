"""
Wrapper runner for explanation metrics analysis with stable output paths.

This module provides a convenient interface to run consistency and correlation analyses
on explanation metrics across multiple experiment runs.

Usage:
    from scripts.explanation_metrics import run_explanation_metrics
    
    status = run_explanation_metrics(
        results_dir="results/runs/python",
        reports_dir="results/reports",
        has_explanations=True,
        pattern="results_run*.json",
        min_runs=2,
    )
    print(status)
"""

import os
import glob
from scripts.standalone.analyze_explanation_metrics import (
    evaluate_consistency,
    analyze_score_passrate_correlation,
)


def run_explanation_metrics(results_dir, reports_dir, has_explanations=True, pattern="results_run*.json", min_runs=2):
    """
    Run explanation metrics analysis with skip rules and stable output paths.
    
    Args:
        results_dir (str): Directory containing results_run*.json files
        reports_dir (str): Directory where output JSON files will be written
        has_explanations (bool): If False, skip the analysis
        pattern (str): Glob pattern to match result files (default: "results_run*.json")
        min_runs (int): Minimum number of runs required to proceed (default: 2)
    
    Returns:
        dict: Status object with keys:
            - "status": "ran", "skipped", or "error"
            - "message": str describing the result or error
    """
    try:
        # Skip rule 1: has_explanations is False
        if not has_explanations:
            return {
                "status": "skipped",
                "message": "has_explanations is False; skipping analysis"
            }
        
        # Discover run count by globbing pattern
        file_paths = sorted(glob.glob(os.path.join(results_dir, pattern)))
        run_count = len(file_paths)
        
        # Skip rule 2: insufficient runs
        if run_count < min_runs:
            return {
                "status": "skipped",
                "message": f"Found {run_count} runs; minimum required is {min_runs}"
            }
        
        # Ensure output directory exists
        os.makedirs(reports_dir, exist_ok=True)
        
        # Define output paths
        consistency_output = os.path.join(reports_dir, "explanation_metrics_consistency.json")
        correlation_output = os.path.join(reports_dir, "explanation_metrics_correlation.json")
        
        # Run consistency analysis
        evaluate_consistency(results_dir, pattern, output_path=consistency_output)
        
        # Run correlation analysis
        analyze_score_passrate_correlation(results_dir, pattern, output_path=correlation_output)
        
        return {
            "status": "ran",
            "message": f"Analysis completed for {run_count} runs; outputs written to {reports_dir}"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Exception during analysis: {str(e)}"
        }
