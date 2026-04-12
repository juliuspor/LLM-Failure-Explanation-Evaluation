# -*- coding: utf-8 -*-
"""
Test for hit07_classutils.py (ClassUtils.to_class)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit07_classutils import ClassUtils


def test_to_class_with_none():
    """
    Test that to_class handles arrays with None elements.
    
    Java equivalent:
    assertTrue(Arrays.equals(
        new Class[] { String.class, null, Double.class },
        ClassUtils.toClass(new Object[] { "Test", null, 99d })
    ));
    """
    test_array = ["Test", None, 99.0]
    expected = [str, type(None), float]
    
    result = ClassUtils.to_class(test_array)
    assert result == expected, f"Expected {expected}, got {result}"


if __name__ == "__main__":
    try:
        test_to_class_with_none()
        print("Test passed!")
    except AttributeError as e:
        print(f"Test failed with AttributeError: {e}")
        sys.exit(1)
