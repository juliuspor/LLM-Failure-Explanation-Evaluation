"""
Script to validate generated fixes against the defect test suite.
Decoupled from the main generation pipeline for safety and efficiency.

Usage:
    python scripts/validate_fixes.py
"""

import os
import sys
import json
import glob
from datetime import datetime

# Add project root to sys.path before importing from scripts/src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import python_defects
from src.validation import FixValidator

RESULTS_DIR = "results/runs/python"

def get_defect_info(defect_id: str):
    """Find defect metadata by ID."""
    for defect in python_defects:
        if defect["id"] == defect_id:
            return defect
    return None

def main():
    print(f"\n{'='*60}")
    print(f"VALIDATION PIPELINE: Scanning {RESULTS_DIR}")
    print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}\n")

    if not os.path.exists(RESULTS_DIR):
        print(f"Error: Results directory '{RESULTS_DIR}' does not exist.")
        return

    validator = FixValidator()
    
    # Find all generated fix files: [defect_id]_[levels]_run[id]_fix.py
    fix_files = glob.glob(os.path.join(RESULTS_DIR, "*_fix.py"))
    
    if not fix_files:
        print("No fix files found. Run the generation pipeline first.")
        return

    results = []
    
    for i, fix_path in enumerate(fix_files, 1):
        filename = os.path.basename(fix_path)
        print(f"[{i}/{len(fix_files)}] Validating {filename}...", end=" ", flush=True)
        
        # Parse filename to get defect ID
        # Format: defect1_py_CODE_run1_fix.py
        # We need to extract 'defect1_py'
        # Simple heuristic: split by first underscore if format is consistent, 
        # but here we have 'defect1_py' (contains underscore).
        # We can accept that IDs are prefixes.
        
        defect = None
        for d in python_defects:
            if filename.startswith(d["id"]):
                defect = d
                break
        
        if not defect:
            print("SKIPPED (Unknown Defect ID)")
            continue
            
        # Determine strict module name expected by test
        # e.g. 'failures/python_defects/hit01_timezone.py' -> 'hit01_timezone'
        original_module_name = os.path.splitext(os.path.basename(defect["source_path"]))[0]
        
        # Validate
        result = validator.validate(
            fix_path=fix_path,
            test_path=defect["test_path"],
            module_name=original_module_name
        )
        
        if result["passed"]:
            print("PASS ✓")
        else:
            print("FAIL ✗")
            
        results.append({
            "fix_file": filename,
            "defect_id": defect["id"],
            "passed": result["passed"],
            "output": result["output"],
            "error": result["error"]
        })
        
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(RESULTS_DIR, f"validation_summary_{timestamp}.json")
    
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
        
    # Print Summary
    num_passed = sum(1 for r in results if r["passed"])
    print(f"\n{'='*60}")
    print(f"SUMMARY: {num_passed}/{len(results)} Passed")
    print(f"Report saved to: {output_path}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
