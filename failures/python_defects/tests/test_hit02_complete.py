# -*- coding: utf-8 -*-
"""
Test for hit02_grayscale.py (GrayPaintScale.get_paint) - Complete Suite
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Note: We import the class to be tested. 
# We will toggle which file this imports from or we can mock/inject, 
# but for this script let's assume valid 'hit02_grayscale' module.
from hit02_grayscale import GrayPaintScale

class TestGrayPaintScale(unittest.TestCase):
    
    def test_lower_bound_clamping(self):
        """Test that values below lower bound are clamped to lower bound (black)."""
        gps = GrayPaintScale()
        # Java original failure case: -0.5 triggers exception if not clamped
        color = gps.get_paint(-0.5)
        self.assertEqual(color, (0, 0, 0), "Should clamp negative values to black (0,0,0)")

    def test_upper_bound_clamping(self):
        """Test that values above upper bound are clamped to upper bound (white)."""
        gps = GrayPaintScale()
        color = gps.get_paint(1.5)
        self.assertEqual(color, (255, 255, 255), "Should clamp values > 1.0 to white (255,255,255)")

    def test_mid_value_interpolation(self):
        """Test that values inside the range are interpolated correctly."""
        gps = GrayPaintScale()
        
        # 0.5 should be exactly middle gray
        # 0.5 - 0.0 / 1.0 - 0.0 * 255.0 = 127.5 -> 127
        color = gps.get_paint(0.5)
        self.assertEqual(color, (127, 127, 127), "0.5 should map to (127, 127, 127)")
        
        # 0.0 should be black
        self.assertEqual(gps.get_paint(0.0), (0, 0, 0))
        
        # 1.0 should be white
        self.assertEqual(gps.get_paint(1.0), (255, 255, 255))

    def test_custom_bounds(self):
        """Test with custom lower and upper bounds."""
        gps = GrayPaintScale(10.0, 20.0)
        
        # Below 10 -> black
        self.assertEqual(gps.get_paint(5.0), (0, 0, 0))
        # Above 20 -> white
        self.assertEqual(gps.get_paint(25.0), (255, 255, 255))
        # Middle (15) -> gray
        self.assertEqual(gps.get_paint(15.0), (127, 127, 127))

if __name__ == "__main__":
    unittest.main()
