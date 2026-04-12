"""
Minimal test to verify prompt building with all context partitions.
Tests that the Experiment class correctly builds prompts for each context level.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.experiment import Experiment, ContextLevel, CRITERIA_INSTRUCTIONS
from src.data import python_defects

def test_prompt_building():
    """Test prompt building with different context levels for defect1."""
    
    # Use first defect for testing
    defect = python_defects[0]
    print(f"\n{'='*60}")
    print(f"Testing prompt building for: {defect['id']}")
    print(f"Source: {defect['source_path']}")
    print(f"Test: {defect['test_path']}")
    print(f"{'='*60}\n")
    
    exp = Experiment(defect)
    
    # Test each context level individually
    test_levels = [
        ("CODE", ContextLevel.CODE),
        ("ERROR", ContextLevel.ERROR),
        ("TEST", ContextLevel.TEST),
        ("DOCSTRING", ContextLevel.DOCSTRING),
        ("SLICE_BLOCK", ContextLevel.SLICE_BLOCK),
        ("SLICE_BACKWARD", ContextLevel.SLICE_BACKWARD),
        ("SLICE_FORWARD", ContextLevel.SLICE_FORWARD),
        ("SLICE_UNION", ContextLevel.SLICE_UNION),
    ]
    
    results = []
    
    for name, level in test_levels:
        print(f"\n--- Testing {name} ---")
        try:
            prompt = exp.get_prompt(level)
            
            # Validate expected sections
            has_section = f"[{name.replace('_', '_')}]" in prompt if name.startswith("SLICE") else f"[{name}]" in prompt
            
            # For slices, check the section name format
            if name.startswith("SLICE_"):
                strategy = name.replace("SLICE_", "")
                has_section = f"[SLICE_{strategy}]" in prompt
            
            print(f"  ✓ Prompt length: {len(prompt)} chars")
            print(f"  ✓ Has [{name}] section: {has_section}")
            print(f"  ✓ Has criteria instructions: {CRITERIA_INSTRUCTIONS.strip()[:50] + '...' in prompt}")
            
            # Print full prompt
            print(f"\n  === FULL PROMPT ===")
            print(prompt)
            print("  === END ===\n")
            
            results.append((name, "PASS", len(prompt)))
            
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            results.append((name, f"FAIL: {e}", 0))
    
    # Test combined levels
    print(f"\n{'='*60}")
    print("Testing combined levels: CODE | ERROR | TEST")
    print(f"{'='*60}")
    
    try:
        combined = ContextLevel.CODE | ContextLevel.ERROR | ContextLevel.TEST
        prompt = exp.get_prompt(combined)
        
        print(f"  ✓ Prompt length: {len(prompt)} chars")
        print(f"  ✓ Has [CODE] section: {'[CODE]' in prompt}")
        print(f"  ✓ Has [ERROR] section: {'[ERROR]' in prompt}")
        print(f"  ✓ Has [TEST] section: {'[TEST]' in prompt}")
        
        # Print the full combined prompt structure
        print(f"\n  === FULL COMBINED PROMPT STRUCTURE ===")
        # Show just the section headers
        for line in prompt.split('\n'):
            if line.startswith('[') and line.endswith(']'):
                print(f"  {line}")
        
        print(f"\n  === FULL PROMPT ===")
        print(prompt)
        
        results.append(("CODE|ERROR|TEST", "PASS", len(prompt)))
        
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        results.append(("CODE|ERROR|TEST", f"FAIL: {e}", 0))
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for name, status, length in results:
        status_icon = "✓" if status == "PASS" else "✗"
        print(f"  {status_icon} {name}: {status} ({length} chars)")
    
    passed = sum(1 for _, status, _ in results if status == "PASS")
    print(f"\n{passed}/{len(results)} tests passed")
    
    return passed == len(results)


if __name__ == "__main__":
    success = test_prompt_building()
    sys.exit(0 if success else 1)
