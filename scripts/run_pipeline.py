"""
Full evaluation pipeline: experiments + evaluation + report generation.

Usage:
    python scripts/run_pipeline.py                        # 1 run, default levels
    python scripts/run_pipeline.py --runs 3               # 3 runs
    python scripts/run_pipeline.py --levels CODE,ERROR    # Custom levels
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Add project root to sys.path before importing from scripts/src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts._common import load_env

from src.validation import FixValidator
from src.experiment import Experiment, ContextLevel, parse_levels
from src.llm import LLMService
from src.evaluation import ExplanationEvaluator
from src.fix import FixGenerator
from src import python_defects
from scripts.explanation_metrics import run_explanation_metrics

load_env(override=True)

RESULTS_DIR = "results/runs"
REPORTS_DIR = "results/reports"

# All 8 isolated context levels
ISOLATED_LEVELS = [
    ContextLevel.CODE,
    ContextLevel.ERROR,
    ContextLevel.TEST,
    ContextLevel.DOCSTRING,
    ContextLevel.SLICE_BLOCK,
    ContextLevel.SLICE_BACKWARD,
    ContextLevel.SLICE_FORWARD,
    ContextLevel.SLICE_UNION,
]

# Configuration: 8 isolated levels + baseline (9 total)
DEFAULT_LEVEL_CONFIGS = ISOLATED_LEVELS.copy()

# Baseline: All levels combined
BASELINE_CONFIG = ContextLevel.NONE
for level in ISOLATED_LEVELS:
    BASELINE_CONFIG |= level

DEFAULT_LEVEL_CONFIGS.append(BASELINE_CONFIG)


def run_pipeline(num_runs: int = 1, level_configs: list = None, no_explanation_baseline: bool = False):
    """
    Run full pipeline:
    1. Generate explanations for all defects × context levels (unless no_explanation_baseline)
    2. Evaluate each explanation
    3. Generate comparison report
    
    Args:
        num_runs: Number of runs per configuration
        level_configs: List of context level configurations
        no_explanation_baseline: If True, skip explanation generation and use direct fix
    """
    if level_configs is None:
        level_configs = DEFAULT_LEVEL_CONFIGS
    
    llm_service = LLMService()
    evaluator = ExplanationEvaluator(llm_service)
    fix_generator = FixGenerator(llm_service)
    validator = FixValidator()
    
    mode_str = "NO-EXPLANATION BASELINE" if no_explanation_baseline else "STANDARD"
    total_calls = len(python_defects) * num_runs * (1 if no_explanation_baseline else len(level_configs) * 3)
    print(f"\n{'='*60}")
    print(f"PIPELINE ({mode_str}): {num_runs} run(s) × {len(python_defects)} defects")
    if not no_explanation_baseline:
        print(f"Configs: {[Experiment.levels_to_string(c) for c in level_configs]}")
    print(f"Estimated LLM calls: {total_calls}")
    print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}\n")
    
    output_dir = os.path.join(RESULTS_DIR, "python")
    os.makedirs(output_dir, exist_ok=True)
    
    for run_id in range(1, num_runs + 1):
        print(f"\n--- Run {run_id}/{num_runs} ---")
        results = []
        
        for defect in python_defects:
            exp = Experiment(defect)
            ground_truth = defect.get("ground_truth", "")
            function_name = defect.get("function_name")
            
            if no_explanation_baseline:
                # NO-EXPLANATION BASELINE: Direct fix from source code only
                levels_name = "NO_EXPLANATION"
                label = f"{defect['id']}/{levels_name}"
                print(f"  {label}...", end=" ", flush=True)
                
                try:
                    # Generate Fix directly (no explanation)
                    fix_result = fix_generator.generate_direct(exp.source_code, function_name)
                    fix_code = fix_result["code"]
                    fix_raw = fix_result["raw_fix"]
                    fix_thought = fix_result["thought_process"]
                    
                    fix_path = os.path.join(output_dir, f"{defect['id']}_{levels_name}_run{run_id}_fix.py")
                    with open(fix_path, "w") as f:
                        f.write(fix_code)
                    
                    raw_path = os.path.join(output_dir, f"{defect['id']}_{levels_name}_run{run_id}_fix_raw.py")
                    with open(raw_path, "w") as f:
                        f.write(fix_raw)
                        
                    thought_path = os.path.join(output_dir, f"{defect['id']}_{levels_name}_run{run_id}_fix_thought.txt")
                    with open(thought_path, "w") as f:
                        f.write(fix_thought)
                    
                    results.append({
                        "defect_id": defect["id"],
                        "language": "python",
                        "levels": levels_name,
                        "run_id": run_id,
                        "scores": None,  # No explanation to evaluate
                        "fix_file": f"{defect['id']}_{levels_name}_run{run_id}_fix.py",
                        "slice_lines": None,
                        "explanation_used": False
                    })
                    
                    # Validate Fix
                    try:
                        original_module_name = os.path.splitext(os.path.basename(defect["source_path"]))[0]
                        validation_result = validator.validate(
                            fix_path=fix_path,
                            test_path=defect["test_path"],
                            module_name=original_module_name
                        )
                        results[-1]["validation"] = {
                            "passed": validation_result["passed"],
                            "output": validation_result["output"],
                            "error": validation_result["error"]
                        }
                    except Exception as ve:
                        results[-1]["validation"] = {
                            "passed": False,
                            "output": "",
                            "error": f"Harness Error: {str(ve)}"
                        }
                    print("✓")
                except Exception as e:
                    print(f"✗ {e}")
            else:
                # STANDARD MODE: Generate explanation, then fix
                for levels in level_configs:
                    levels_name = Experiment.levels_to_string(levels)
                    label = f"{defect['id']}/{levels_name}"
                    print(f"  {label}...", end=" ", flush=True)
                    
                    try:
                        # Generate explanation
                        explanation = exp.run(levels, llm_service)
                        
                        # Save explanation
                        output_path = os.path.join(output_dir, f"{defect['id']}_{levels_name}_run{run_id}.txt")
                        with open(output_path, "w") as f:
                            f.write(explanation)
                        
                        # Generate Fix
                        try:
                            fix_result = fix_generator.generate(exp.source_code, explanation, function_name=function_name)
                            fix_code = fix_result["code"]
                            fix_raw = fix_result["raw_fix"]
                            fix_thought = fix_result["thought_process"]
                            
                            fix_path = os.path.join(output_dir, f"{defect['id']}_{levels_name}_run{run_id}_fix.py")
                            with open(fix_path, "w") as f:
                                f.write(fix_code)
                            
                            raw_path = os.path.join(output_dir, f"{defect['id']}_{levels_name}_run{run_id}_fix_raw.py")
                            with open(raw_path, "w") as f:
                                f.write(fix_raw)
                                
                            thought_path = os.path.join(output_dir, f"{defect['id']}_{levels_name}_run{run_id}_fix_thought.txt")
                            with open(thought_path, "w") as f:
                                f.write(fix_thought)
                                
                        except Exception as e:
                            print(f"Warning: Fix generation failed: {e}")
                        
                        # Evaluate
                        scores = evaluator.evaluate(explanation, ground_truth)
                        
                        # Collect slice line numbers for any slice strategies used
                        slice_lines_info = {}
                        for slice_level in [ContextLevel.SLICE_BLOCK, ContextLevel.SLICE_BACKWARD, 
                                            ContextLevel.SLICE_FORWARD, ContextLevel.SLICE_UNION]:
                            if slice_level in levels:
                                slice_lines_info[slice_level.name] = sorted(list(exp.get_slice_lines(slice_level)))
                        
                        results.append({
                            "defect_id": defect["id"],
                            "language": "python",
                            "levels": levels_name,
                            "run_id": run_id,
                            "scores": scores,
                            "fix_file": f"{defect['id']}_{levels_name}_run{run_id}_fix.py",
                            "slice_lines": slice_lines_info if slice_lines_info else None,
                            "explanation_used": True
                        })
                        # Validate Fix (Graceful Failure)
                        try:
                            # Determine module name for test import
                            original_module_name = os.path.splitext(os.path.basename(defect["source_path"]))[0]
                            fix_path = os.path.join(output_dir, f"{defect['id']}_{levels_name}_run{run_id}_fix.py")
                            
                            validation_result = validator.validate(
                                fix_path=fix_path,
                                test_path=defect["test_path"],
                                module_name=original_module_name
                            )
                            results[-1]["validation"] = {
                                "passed": validation_result["passed"],
                                "output": validation_result["output"],
                                "error": validation_result["error"]
                            }
                        except Exception as ve:
                            results[-1]["validation"] = {
                                "passed": False,
                                "output": "",
                                "error": f"Harness Error: {str(ve)}"
                            }
                        print("✓")
                    except Exception as e:
                        print(f"✗ {e}")
        
        # Save run results
        results_path = os.path.join(output_dir, f"results_run{run_id}.json")
        with open(results_path, "w") as f:
            json.dump(results, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"PIPELINE COMPLETE: {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}")
    print("\nGenerating report...")
    
    # Import and run report generation
    from scripts.generate_report import (
        load_results, aggregate_scores, aggregate_by_defect, 
        save_csv, save_defect_csv, plot_comparison_bars, plot_heatmaps, plot_defect_charts,
        plot_run_variance, aggregate_fix_results, save_fix_csv, plot_fix_success_rates,
        plot_fix_quality_metrics, plot_changed_lines_comparison,
        compare_with_ground_truth
    )
    
    python_results = load_results("python")
    
    if python_results:
        # Run ground truth comparison and update JSON files
        python_path = os.path.join(RESULTS_DIR, "python")
        print("Comparing fixes with ground truth...")
        
        # Load JSON files for updating
        json_files = {}
        for filename in os.listdir(python_path):
            if filename.startswith("results") and filename.endswith(".json"):
                file_path = os.path.join(python_path, filename)
                with open(file_path) as f:
                    json_files[file_path] = json.load(f)
        
        # Compare each fix with ground truth (all entries, not just passing)
        modified_files = set()
        for entry in python_results:
            defect_id = entry.get("defect_id")
            fix_file = entry.get("fix_file")
            slice_lines_info = entry.get("slice_lines", {})
            
            if defect_id and fix_file:
                comparison_result = compare_with_ground_truth(
                    defect_id, python_path, fix_file, slice_lines_info
                )
                if comparison_result is not None:
                    if entry.get("comparison") != comparison_result:
                        entry["comparison"] = comparison_result
                        # Find which file this entry belongs to and mark as modified
                        for file_path, file_data in json_files.items():
                            if entry in file_data:
                                modified_files.add(file_path)
        
        # Save updated JSON files
        for file_path in modified_files:
            with open(file_path, "w") as f:
                json.dump(json_files[file_path], f, indent=2)
            print(f"Updated: {file_path}")
        
        python_agg = aggregate_scores(python_results)
        python_by_defect = aggregate_by_defect(python_results)
        fix_agg = aggregate_fix_results(python_results)
        
        os.makedirs(REPORTS_DIR, exist_ok=True)
        save_csv(python_agg, os.path.join(REPORTS_DIR, "comparison.csv"))
        save_defect_csv(python_by_defect, os.path.join(REPORTS_DIR, "defect_breakdown.csv"))
        save_fix_csv(fix_agg, os.path.join(REPORTS_DIR, "fix_results.csv"))
        plot_comparison_bars(python_agg, REPORTS_DIR)
        plot_heatmaps(python_agg, REPORTS_DIR)
        plot_defect_charts(python_by_defect, REPORTS_DIR)
        plot_fix_success_rates(fix_agg, REPORTS_DIR)
        plot_fix_quality_metrics(fix_agg, REPORTS_DIR)
        plot_changed_lines_comparison(fix_agg, REPORTS_DIR)
        plot_run_variance(python_results, REPORTS_DIR)
        
        print(f"\n✓ Reports saved to {REPORTS_DIR}/")
    
    # Run explanation metrics analysis if we have multiple runs with explanations
    if num_runs >= 2:
        try:
            python_results_dir = os.path.join(RESULTS_DIR, "python")
            metrics_result = run_explanation_metrics(
                results_dir=python_results_dir,
                reports_dir=REPORTS_DIR,
                has_explanations=not no_explanation_baseline,
                min_runs=2
            )
            if metrics_result["status"] == "ran":
                print(f"✓ Explanation metrics: {metrics_result['message']}")
            elif metrics_result["status"] == "skipped":
                print(f"⊘ Explanation metrics: {metrics_result['message']}")
            else:  # error
                print(f"⚠ Warning: Explanation metrics failed: {metrics_result['message']}")
        except Exception as e:
            print(f"⚠ Warning: Explanation metrics wrapper failed: {str(e)}")



if __name__ == "__main__":
    from scripts._common import add_runs_argument
    
    parser = argparse.ArgumentParser(description="Run full evaluation pipeline")
    add_runs_argument(parser)
    parser.add_argument("--levels", help="Comma-separated context levels (e.g., CODE,ERROR,TEST)")
    parser.add_argument("--no-explanation-baseline", action="store_true", 
                        help="Run baseline without explanation generation (direct fix from source only)")
    args = parser.parse_args()
    
    level_configs = None
    if args.levels:
        level_configs = [parse_levels(args.levels)]
    
    run_pipeline(num_runs=args.runs, level_configs=level_configs, 
                 no_explanation_baseline=args.no_explanation_baseline)
