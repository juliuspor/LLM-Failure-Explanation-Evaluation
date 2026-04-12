"""
Minimal unit tests for explanation_metrics integration.

Tests the wrapper function `run_explanation_metrics` from scripts.explanation_metrics
with synthetic fixtures in temporary directories. Uses stdlib unittest only.

Test Coverage:
  1. Build synthetic results with multiple (defect_id, levels) entries and scores
  2. Verify output JSON files exist and have expected top-level keys
  3. Test skip on runs < 2
  4. Test skip on has_explanations=False
  5. Test warn+continue behavior with forced exception
"""

import unittest
import tempfile
import shutil
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))


class TestExplanationMetricsIntegration(unittest.TestCase):
    """Integration tests for explanation_metrics wrapper."""

    def setUp(self):
        """Create temporary directory for each test."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_results_json(self, filepath, entries):
        """Helper: Create a results_run*.json with given entries."""
        with open(filepath, 'w') as f:
            json.dump(entries, f)

    def _build_result_entry(self, defect_id, levels, scores, validation_passed=True, run_id=None):
        """Helper: Build a single result entry with all expected fields."""
        return {
            "defect_id": defect_id,
            "levels": levels,
            "scores": {
                "C1_Readability": scores.get("C1_Readability", 1),
                "C2_Problem_Identification": scores.get("C2_Problem_Identification", 1),
                "C3_Explanation_Clarity": scores.get("C3_Explanation_Clarity", 1),
                "C4_Actionability": scores.get("C4_Actionability", 1),
                "C5_Contextual_Adequacy": scores.get("C5_Contextual_Adequacy", 1),
                "C6_Brevity": scores.get("C6_Brevity", 1),
            },
            "validation": {
                "passed": validation_passed
            },
            "run_id": run_id or 1
        }

    def test_01_two_runs_consistency_output(self):
        """Test: Two runs produce consistency JSON with expected structure."""
        # Import here to avoid issues if module doesn't exist
        from scripts.explanation_metrics import run_explanation_metrics

        # Build temp results_dir and reports_dir
        results_dir = os.path.join(self.temp_dir, "results")
        reports_dir = os.path.join(self.temp_dir, "reports")
        os.makedirs(results_dir, exist_ok=True)

        # Create results_run1.json with multiple entries
        run1_entries = [
            self._build_result_entry("d1", "CODE", {"C1": 1, "C2": 1, "C3": 1, "C4": 1, "C5": 1, "C6": 1}, run_id=1),
            self._build_result_entry("d1", "CODE|ERROR", {"C1": 1, "C2": 0, "C3": 1, "C4": 1, "C5": 1, "C6": 1}, run_id=1),
            self._build_result_entry("d2", "CODE", {"C1": 1, "C2": 1, "C3": 1, "C4": 1, "C5": 1, "C6": 1}, run_id=1),
        ]
        self._create_results_json(os.path.join(results_dir, "results_run1.json"), run1_entries)

        # Create results_run2.json with matching entries (same structure, run_id=2)
        run2_entries = [
            self._build_result_entry("d1", "CODE", {"C1": 1, "C2": 1, "C3": 1, "C4": 1, "C5": 1, "C6": 1}, run_id=2),
            self._build_result_entry("d1", "CODE|ERROR", {"C1": 1, "C2": 1, "C3": 1, "C4": 1, "C5": 1, "C6": 1}, run_id=2),
            self._build_result_entry("d2", "CODE", {"C1": 1, "C2": 1, "C3": 1, "C4": 1, "C5": 1, "C6": 1}, run_id=2),
        ]
        self._create_results_json(os.path.join(results_dir, "results_run2.json"), run2_entries)

        # Call wrapper
        result = run_explanation_metrics(
            results_dir=results_dir,
            reports_dir=reports_dir,
            has_explanations=True,
            min_runs=2
        )

        # Verify status
        self.assertEqual(result["status"], "ran", f"Expected status='ran', got {result}")

        # Verify consistency output file exists and has expected keys
        consistency_file = os.path.join(reports_dir, "explanation_metrics_consistency.json")
        self.assertTrue(os.path.exists(consistency_file), f"Consistency file not created: {consistency_file}")

        with open(consistency_file, 'r') as f:
            consistency_data = json.load(f)

        self.assertIn("metadata", consistency_data)
        self.assertIn("overall", consistency_data)
        self.assertIn("per_level", consistency_data)
        self.assertIn("criteria", consistency_data["metadata"])

    def test_02_two_runs_correlation_output(self):
        """Test: Two runs produce correlation JSON with expected structure."""
        from scripts.explanation_metrics import run_explanation_metrics

        results_dir = os.path.join(self.temp_dir, "results")
        reports_dir = os.path.join(self.temp_dir, "reports")
        os.makedirs(results_dir, exist_ok=True)

        # Create results with validation data
        run1_entries = [
            self._build_result_entry("d1", "CODE", {"C1": 1, "C2": 1, "C3": 1, "C4": 1, "C5": 1, "C6": 1}, validation_passed=True, run_id=1),
            self._build_result_entry("d2", "CODE", {"C1": 0, "C2": 0, "C3": 0, "C4": 0, "C5": 0, "C6": 0}, validation_passed=False, run_id=1),
        ]
        self._create_results_json(os.path.join(results_dir, "results_run1.json"), run1_entries)

        run2_entries = [
            self._build_result_entry("d1", "CODE", {"C1": 1, "C2": 1, "C3": 1, "C4": 1, "C5": 1, "C6": 1}, validation_passed=True, run_id=2),
            self._build_result_entry("d2", "CODE", {"C1": 0, "C2": 0, "C3": 0, "C4": 0, "C5": 0, "C6": 0}, validation_passed=False, run_id=2),
        ]
        self._create_results_json(os.path.join(results_dir, "results_run2.json"), run2_entries)

        # Call wrapper
        result = run_explanation_metrics(
            results_dir=results_dir,
            reports_dir=reports_dir,
            has_explanations=True,
            min_runs=2
        )

        self.assertEqual(result["status"], "ran")

        # Verify correlation output file exists
        correlation_file = os.path.join(reports_dir, "explanation_metrics_correlation.json")
        self.assertTrue(os.path.exists(correlation_file), f"Correlation file not created: {correlation_file}")

        with open(correlation_file, 'r') as f:
            correlation_data = json.load(f)

        self.assertIn("metadata", correlation_data)
        self.assertIn("level_ranking", correlation_data)
        self.assertIn("quartile_analysis", correlation_data)
        self.assertIn("criterion_correlation", correlation_data)
        self.assertIn("insights", correlation_data)

    def test_03_skip_on_single_run(self):
        """Test: Skip analysis when only 1 run is found."""
        from scripts.explanation_metrics import run_explanation_metrics

        results_dir = os.path.join(self.temp_dir, "results")
        reports_dir = os.path.join(self.temp_dir, "reports")
        os.makedirs(results_dir, exist_ok=True)

        # Create only one results file
        run1_entries = [
            self._build_result_entry("d1", "CODE", {"C1": 1, "C2": 1, "C3": 1, "C4": 1, "C5": 1, "C6": 1}, run_id=1),
        ]
        self._create_results_json(os.path.join(results_dir, "results_run1.json"), run1_entries)

        # Call wrapper with min_runs=2 (default)
        result = run_explanation_metrics(
            results_dir=results_dir,
            reports_dir=reports_dir,
            has_explanations=True,
            min_runs=2
        )

        # Should skip
        self.assertEqual(result["status"], "skipped")
        self.assertIn("minimum required", result["message"])

        # No output files should be created
        consistency_file = os.path.join(reports_dir, "explanation_metrics_consistency.json")
        correlation_file = os.path.join(reports_dir, "explanation_metrics_correlation.json")
        self.assertFalse(os.path.exists(consistency_file))
        self.assertFalse(os.path.exists(correlation_file))

    def test_04_skip_on_has_explanations_false(self):
        """Test: Skip analysis when has_explanations=False."""
        from scripts.explanation_metrics import run_explanation_metrics

        results_dir = os.path.join(self.temp_dir, "results")
        reports_dir = os.path.join(self.temp_dir, "reports")
        os.makedirs(results_dir, exist_ok=True)

        # Create two results files (sufficient for runs, but has_explanations=False)
        run1_entries = [
            self._build_result_entry("d1", "CODE", {"C1": 1, "C2": 1, "C3": 1, "C4": 1, "C5": 1, "C6": 1}, run_id=1),
        ]
        self._create_results_json(os.path.join(results_dir, "results_run1.json"), run1_entries)

        run2_entries = [
            self._build_result_entry("d1", "CODE", {"C1": 1, "C2": 1, "C3": 1, "C4": 1, "C5": 1, "C6": 1}, run_id=2),
        ]
        self._create_results_json(os.path.join(results_dir, "results_run2.json"), run2_entries)

        # Call with has_explanations=False
        result = run_explanation_metrics(
            results_dir=results_dir,
            reports_dir=reports_dir,
            has_explanations=False,
            min_runs=2
        )

        # Should skip due to has_explanations flag
        self.assertEqual(result["status"], "skipped")
        self.assertIn("has_explanations is False", result["message"])

        # No output files should be created
        consistency_file = os.path.join(reports_dir, "explanation_metrics_consistency.json")
        correlation_file = os.path.join(reports_dir, "explanation_metrics_correlation.json")
        self.assertFalse(os.path.exists(consistency_file))
        self.assertFalse(os.path.exists(correlation_file))

    def test_05_skip_on_scores_none(self):
        """Test: Skip analysis when entries have scores=None (no explanations)."""
        from scripts.explanation_metrics import run_explanation_metrics

        results_dir = os.path.join(self.temp_dir, "results")
        reports_dir = os.path.join(self.temp_dir, "reports")
        os.makedirs(results_dir, exist_ok=True)

        # Create entries with scores=None (baseline mode)
        run1_entries = [
            {
                "defect_id": "d1",
                "levels": "CODE",
                "scores": None,  # No explanations in baseline
                "validation": {"passed": False},
                "run_id": 1
            }
        ]
        self._create_results_json(os.path.join(results_dir, "results_run1.json"), run1_entries)

        run2_entries = [
            {
                "defect_id": "d1",
                "levels": "CODE",
                "scores": None,
                "validation": {"passed": False},
                "run_id": 2
            }
        ]
        self._create_results_json(os.path.join(results_dir, "results_run2.json"), run2_entries)

        # The wrapper checks has_explanations flag, not scores content
        # When called with has_explanations=False (baseline mode), it skips
        result = run_explanation_metrics(
            results_dir=results_dir,
            reports_dir=reports_dir,
            has_explanations=False,
            min_runs=2
        )

        self.assertEqual(result["status"], "skipped")

    def test_06_error_handling_continues_gracefully(self):
        """Test: Wrapper returns error status without raising exception."""
        from scripts.explanation_metrics import run_explanation_metrics

        # Create invalid results directory structure
        results_dir = os.path.join(self.temp_dir, "results_bad")
        reports_dir = os.path.join(self.temp_dir, "reports_bad")
        os.makedirs(results_dir, exist_ok=True)

        # Create malformed JSON files to trigger analysis exception
        with open(os.path.join(results_dir, "results_run1.json"), 'w') as f:
            f.write("{ invalid json")

        with open(os.path.join(results_dir, "results_run2.json"), 'w') as f:
            f.write("{ another invalid }")

        # Call wrapper - should return error status, not raise exception
        result = run_explanation_metrics(
            results_dir=results_dir,
            reports_dir=reports_dir,
            has_explanations=True,
            min_runs=2
        )

        # Should return error status, not raise
        self.assertEqual(result["status"], "error")
        self.assertIn("Exception", result["message"])

    def test_07_output_dir_created_if_missing(self):
        """Test: Output directory is created if it doesn't exist."""
        from scripts.explanation_metrics import run_explanation_metrics

        results_dir = os.path.join(self.temp_dir, "results")
        reports_dir = os.path.join(self.temp_dir, "nonexistent", "reports")
        os.makedirs(results_dir, exist_ok=True)

        # Create results
        run1_entries = [
            self._build_result_entry("d1", "CODE", {"C1": 1, "C2": 1, "C3": 1, "C4": 1, "C5": 1, "C6": 1}, run_id=1),
        ]
        self._create_results_json(os.path.join(results_dir, "results_run1.json"), run1_entries)

        run2_entries = [
            self._build_result_entry("d1", "CODE", {"C1": 1, "C2": 1, "C3": 1, "C4": 1, "C5": 1, "C6": 1}, run_id=2),
        ]
        self._create_results_json(os.path.join(results_dir, "results_run2.json"), run2_entries)

        # Verify reports_dir doesn't exist yet
        self.assertFalse(os.path.exists(reports_dir))

        # Call wrapper
        result = run_explanation_metrics(
            results_dir=results_dir,
            reports_dir=reports_dir,
            has_explanations=True,
            min_runs=2
        )

        # Should succeed and create dir
        self.assertEqual(result["status"], "ran")
        self.assertTrue(os.path.exists(reports_dir))

    def test_08_multiple_context_levels(self):
        """Test: Multiple different context levels are processed correctly."""
        from scripts.explanation_metrics import run_explanation_metrics

        results_dir = os.path.join(self.temp_dir, "results")
        reports_dir = os.path.join(self.temp_dir, "reports")
        os.makedirs(results_dir, exist_ok=True)

        # Create entries with various context levels
        run1_entries = [
            self._build_result_entry("d1", "CODE", {"C1": 1, "C2": 1, "C3": 1, "C4": 1, "C5": 1, "C6": 1}, run_id=1),
            self._build_result_entry("d1", "CODE|ERROR", {"C1": 1, "C2": 1, "C3": 0, "C4": 1, "C5": 1, "C6": 1}, run_id=1),
            self._build_result_entry("d1", "CODE|ERROR|TEST", {"C1": 0, "C2": 1, "C3": 1, "C4": 1, "C5": 1, "C6": 1}, run_id=1),
            self._build_result_entry("d2", "SLICE_BACKWARD", {"C1": 1, "C2": 0, "C3": 1, "C4": 1, "C5": 0, "C6": 1}, run_id=1),
        ]
        self._create_results_json(os.path.join(results_dir, "results_run1.json"), run1_entries)

        run2_entries = [
            self._build_result_entry("d1", "CODE", {"C1": 1, "C2": 1, "C3": 1, "C4": 1, "C5": 1, "C6": 1}, run_id=2),
            self._build_result_entry("d1", "CODE|ERROR", {"C1": 1, "C2": 1, "C3": 0, "C4": 1, "C5": 1, "C6": 1}, run_id=2),
            self._build_result_entry("d1", "CODE|ERROR|TEST", {"C1": 0, "C2": 1, "C3": 1, "C4": 1, "C5": 1, "C6": 1}, run_id=2),
            self._build_result_entry("d2", "SLICE_BACKWARD", {"C1": 1, "C2": 0, "C3": 1, "C4": 1, "C5": 0, "C6": 1}, run_id=2),
        ]
        self._create_results_json(os.path.join(results_dir, "results_run2.json"), run2_entries)

        result = run_explanation_metrics(
            results_dir=results_dir,
            reports_dir=reports_dir,
            has_explanations=True,
            min_runs=2
        )

        self.assertEqual(result["status"], "ran")

        # Verify per_level data exists and contains multiple levels
        consistency_file = os.path.join(reports_dir, "explanation_metrics_consistency.json")
        with open(consistency_file, 'r') as f:
            consistency_data = json.load(f)

        per_level = consistency_data.get("per_level", {})
        self.assertGreater(len(per_level), 0, "Expected multiple context levels in output")


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
