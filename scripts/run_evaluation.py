"""
Multi-run evaluation for variance analysis.
"""

import os
import sys
import json
import argparse

# Add project root to sys.path before importing from scripts/src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts._common import load_env

from src import Experiment, ContextLevel, python_defects, LLMService, ExplanationEvaluator, parse_levels

load_env(override=False)


def run_evaluation(num_runs: int, levels: ContextLevel = None, defect_ids: list = None):
    """Run multi-run evaluation with specified context levels."""
    llm_service = LLMService()
    evaluator = ExplanationEvaluator(llm_service)
    
    if levels is None:
        levels = ContextLevel.CODE | ContextLevel.ERROR | ContextLevel.TEST
    
    output_dir = "results/runs/python"
    os.makedirs(output_dir, exist_ok=True)
    
    target_defects = [d for d in python_defects if defect_ids is None or d['id'] in defect_ids]
    levels_name = Experiment.levels_to_string(levels)
    
    print(f"\nPYTHON | {len(target_defects)} defects | {levels_name} | {num_runs} runs")
    
    for run_id in range(1, num_runs + 1):
        print(f"\n{'='*60}\nRUN {run_id}/{num_runs}\n{'='*60}")
        
        results = []
        
        for defect in target_defects:
            exp = Experiment(defect)
            ground_truth = defect.get('ground_truth', '')
            
            print(f"  {defect['id']} - {levels_name}...", end=" ")
            try:
                explanation = exp.run(levels, llm_service)
                
                output_path = f"{output_dir}/{defect['id']}_{levels_name}_run{run_id}.txt"
                with open(output_path, "w") as f:
                    f.write(explanation)
                
                scores = evaluator.evaluate(explanation, ground_truth)
                results.append({
                    "defect_id": defect['id'],
                    "language": "python",
                    "levels": levels_name,
                    "run_id": run_id,
                    "scores": scores
                })
                print("✓")
            except Exception as e:
                print(f"✗ {e}")
        
        results_path = f"{output_dir}/results_run{run_id}.json"
        with open(results_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"  Saved: {results_path}")
    
    print(f"\n{'='*60}\nCOMPLETE\n{'='*60}")
    print(f"Report: python scripts/generate_report.py --save-plots --save-csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-run evaluation")
    parser.add_argument("runs", type=int, help="Number of runs")
    parser.add_argument("-d", "--defect", help="Defect ID")
    parser.add_argument("-l", "--levels", default="CODE,ERROR,TEST",
                        help="Comma-separated context levels (default: CODE,ERROR,TEST)")
    args = parser.parse_args()
    
    defect_ids = [args.defect] if args.defect else None
    levels = parse_levels(args.levels)
    
    run_evaluation(args.runs, levels=levels, defect_ids=defect_ids)
