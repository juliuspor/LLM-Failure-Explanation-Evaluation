"""
Run experiments with composable context levels for Python defects.
"""

import os
import sys
import argparse

# Add project root to sys.path before importing from scripts/src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts._common import load_env, add_defect_argument, add_levels_argument

from src import Experiment, ContextLevel, python_defects, LLMService, parse_levels

load_env(override=True)


def run_experiment(defect_ids: list = None, levels: ContextLevel = None):
    """Run experiments with specified context levels."""
    llm_service = LLMService()
    
    if levels is None:
        levels = ContextLevel.CODE | ContextLevel.ERROR | ContextLevel.TEST
    
    output_dir = "results/runs/python"
    os.makedirs(output_dir, exist_ok=True)
    
    target_defects = [d for d in python_defects if defect_ids is None or d['id'] in defect_ids]
    levels_name = Experiment.levels_to_string(levels)
    
    print(f"\nPYTHON | {len(target_defects)} defects | levels: {levels_name}")
    print("=" * 60)
    
    for defect in target_defects:
        exp = Experiment(defect)
        print(f"{defect['id']} - {levels_name}...", end=" ")
        
        try:
            output_text = exp.run(levels, llm_service)
            
            output_path = f"{output_dir}/{defect['id']}_{levels_name}.txt"
            with open(output_path, "w") as f:
                f.write(output_text)
            print("✓")
        except Exception as e:
            print(f"✗ {e}")
    
    print("\nDone.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run experiments with composable context levels")
    add_defect_argument(parser)
    add_levels_argument(parser)
    args = parser.parse_args()
    
    defect_ids = [args.defect] if args.defect else None
    levels = parse_levels(args.levels)
    
    run_experiment(defect_ids=defect_ids, levels=levels)

