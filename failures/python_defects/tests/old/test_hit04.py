# -*- coding: utf-8 -*-
"""
Test for hit04_timeperiod.py (TimePeriodValues._update_bounds)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit04_timeperiod import TimePeriodValues, SimpleTimePeriod


def test_max_middle_index_bug():
    """
    Test that get_max_middle_index returns the correct index.
    
    Java equivalent:
    TimePeriodValues s = new TimePeriodValues("Test");
    s.add(new SimpleTimePeriod(0, 100), 1.0);
    s.add(new SimpleTimePeriod(100, 200), 2.0);
    s.add(new SimpleTimePeriod(0, 50), 3.0);
    s.add(new SimpleTimePeriod(50, 100), 4.0);
    assertEquals(1, s.getMaxMiddleIndex());
    
    Java failure: junit.framework.AssertionFailedError: expected:<1> but was:<3>
    """
    s = TimePeriodValues("Test")
    s.add(SimpleTimePeriod(0, 100), 1.0)
    s.add(SimpleTimePeriod(100, 200), 2.0)
    s.add(SimpleTimePeriod(0, 50), 3.0)
    s.add(SimpleTimePeriod(50, 100), 4.0)
    
    expected = 1
    actual = s.get_max_middle_index()
    assert actual == expected, f"Expected max_middle_index={expected}, got {actual}"


if __name__ == "__main__":
    try:
        test_max_middle_index_bug()
        print("Test passed!")
    except AssertionError as e:
        print(f"Test failed with AssertionError: {e}")
        sys.exit(1)
