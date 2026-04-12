# -*- coding: utf-8 -*-
"""
Test for hit02_grayscale.py (GrayPaintScale.get_paint)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit02_grayscale import GrayPaintScale


def test_get_paint_negative_value():
    """
    Test that get_paint handles values below lower bound.
    
    Java equivalent:
    GrayPaintScale gps = new GrayPaintScale();
    c = (Color) gps.getPaint(-0.5);
    assertTrue(c.equals(Color.black));
    """
    gps = GrayPaintScale()
    color = gps.get_paint(-0.5)
    expected = (0, 0, 0)  # Should clamp to black
    assert color == expected, f"Expected {expected}, got {color}"


if __name__ == "__main__":
    try:
        test_get_paint_negative_value()
        print("Test passed!")
    except ValueError as e:
        print(f"Test failed with ValueError: {e}")
        sys.exit(1)
