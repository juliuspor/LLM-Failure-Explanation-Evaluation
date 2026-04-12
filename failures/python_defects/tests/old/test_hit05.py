# -*- coding: utf-8 -*-
"""
Test for hit05_arrayutils.py (ArrayUtils.add)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit05_arrayutils import ArrayUtils


def test_add_null_to_null():
    """
    Test that add(None, None) handles type expectations correctly.
    
    Java equivalent:
    String[] sa = ArrayUtils.add(stringArray, aString);
    
    Java failure: java.lang.ClassCastException: [Ljava.lang.Object; 
                  cannot be cast to [Ljava.lang.String;
    """
    result = ArrayUtils.add(None, None, expected_type=str)
    assert result == [None], f"Expected [None], got {result}"


if __name__ == "__main__":
    try:
        test_add_null_to_null()
        print("Test passed!")
    except TypeError as e:
        print(f"Test failed with TypeError: {e}")
        sys.exit(1)
