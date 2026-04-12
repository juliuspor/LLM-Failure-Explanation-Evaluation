# -*- coding: utf-8 -*-
"""
Test for hit06_codeconsumer.py (CodeConsumer.add_number)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit06_codeconsumer import CodeConsumer


class MockCodeConsumer(CodeConsumer):
    def __init__(self):
        super().__init__()
        self.code = ""

    def append(self, s):
        self.code += s

    def get_code(self):
        return self.code


def test_negative_zero():
    """
    Test that negative zero is printed as -0.0 to preserve sign.
    
    Java equivalent:
    assertPrint("var x = -0.0;", "var x=-0.0");
    
    Java failure: junit.framework.ComparisonFailure: 
                  expected:<var x=[-0.]0> but was:<var x=[]0>
    """
    cc = MockCodeConsumer()
    cc.add_number(-0.0)
    
    result = cc.get_code()
    assert result == "-0.0", f"Expected -0.0, got {result}"


if __name__ == "__main__":
    try:
        test_negative_zero()
        print("Test passed!")
    except AssertionError as e:
        print(f"Test failed with AssertionError: {e}")
        sys.exit(1)
