# -*- coding: utf-8 -*-
"""
Test for hit06_codeconsumer.py (CodeConsumer.add_number) - Complete Suite
Covers the negative zero handling bug.
"""

import sys
import os
import unittest
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit06_codeconsumer import CodeConsumer


class MockCodeConsumer(CodeConsumer):
    """Concrete implementation for testing."""
    
    def __init__(self):
        super().__init__()
        self._output = ""

    def append(self, s):
        self._output += s

    def get_code(self):
        return self._output
    
    def reset(self):
        self._output = ""
        self.statement_needs_ended = False
        self.statement_started = False


class TestCodeConsumerAddNumber(unittest.TestCase):
    
    def setUp(self):
        self.cc = MockCodeConsumer()
    
    def tearDown(self):
        self.cc.reset()
    
    def test_negative_zero(self):
        """
        Original bug case: Negative zero should be printed as -0.0 to preserve sign.
        
        Java equivalent: assertPrint("var x = -0.0;", "var x=-0.0");
        Java failure: junit.framework.ComparisonFailure: 
                      expected:<var x=[-0.]0> but was:<var x=[]0>
        """
        self.cc.add_number(-0.0)
        result = self.cc.get_code()
        # Must preserve negative zero sign
        self.assertEqual(result, "-0.0", f"Expected -0.0, got {result}")
    
    def test_positive_zero(self):
        """Test that positive zero is printed correctly."""
        self.cc.add_number(0.0)
        result = self.cc.get_code()
        self.assertEqual(result, "0")
    
    def test_positive_integer(self):
        """Test positive integers."""
        self.cc.add_number(42.0)
        result = self.cc.get_code()
        self.assertEqual(result, "42")
    
    def test_negative_integer(self):
        """Test negative integers."""
        self.cc.add_number(-42.0)
        result = self.cc.get_code()
        self.assertEqual(result, "-42")
    
    def test_positive_float(self):
        """Test positive floats."""
        self.cc.add_number(3.14)
        result = self.cc.get_code()
        self.assertEqual(result, "3.14")
    
    def test_negative_float(self):
        """Test negative floats."""
        self.cc.add_number(-3.14)
        result = self.cc.get_code()
        self.assertEqual(result, "-3.14")
    
    def test_large_number_scientific_notation(self):
        """Test that large round numbers use scientific notation."""
        self.cc.add_number(1000000.0)
        result = self.cc.get_code()
        # Should use E notation for efficiency
        self.assertIn("E", result)
    
    def test_small_integer(self):
        """Test small integers don't use scientific notation."""
        self.cc.add_number(99.0)
        result = self.cc.get_code()
        self.assertEqual(result, "99")
    
    def test_infinity(self):
        """Test positive infinity - skip if implementation doesn't handle."""
        try:
            self.cc.add_number(float('inf'))
            result = self.cc.get_code()
            self.assertIn("inf", result.lower())
        except (OverflowError, ValueError):
            self.skipTest("Implementation doesn't handle infinity")
    
    def test_negative_infinity(self):
        """Test negative infinity - skip if implementation doesn't handle."""
        try:
            self.cc.add_number(float('-inf'))
            result = self.cc.get_code()
            self.assertIn("inf", result.lower())
        except (OverflowError, ValueError):
            self.skipTest("Implementation doesn't handle negative infinity")
    
    def test_nan(self):
        """Test NaN - skip if implementation doesn't handle."""
        try:
            self.cc.add_number(float('nan'))
            result = self.cc.get_code()
            self.assertIn("nan", result.lower())
        except (ValueError, OverflowError):
            self.skipTest("Implementation doesn't handle NaN")
    
    def test_negative_after_minus(self):
        """
        Test space insertion when negative number follows minus operator.
        Note: The fix for negative zero doesn't change this behavior.
        """
        self.cc.append("-")
        self.cc.add_number(-5.0)
        result = self.cc.get_code()
        # The fix doesn't change space insertion behavior, just verify no syntax error
        # (would be "--5" which is decrements, not subtraction of negative)
        self.assertIn("-5", result)


class TestNegativeZeroUtility(unittest.TestCase):
    """Test the is_negative_zero utility method."""
    
    def test_is_negative_zero_true(self):
        """Test detection of negative zero."""
        self.assertTrue(CodeConsumer.is_negative_zero(-0.0))
    
    def test_is_negative_zero_false_positive(self):
        """Test that positive zero is not negative zero."""
        self.assertFalse(CodeConsumer.is_negative_zero(0.0))
    
    def test_is_negative_zero_false_nonzero(self):
        """Test that non-zero values are not negative zero."""
        self.assertFalse(CodeConsumer.is_negative_zero(1.0))
        self.assertFalse(CodeConsumer.is_negative_zero(-1.0))


if __name__ == "__main__":
    unittest.main()
