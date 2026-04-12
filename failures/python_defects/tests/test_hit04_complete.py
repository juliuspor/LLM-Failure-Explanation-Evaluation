# -*- coding: utf-8 -*-
"""
Test for hit04_timeperiod.py (TimePeriodValues._update_bounds) - Complete Suite
Covers the max_middle_index bug where wrong index variable is used for comparison.
"""

import sys
import os
import unittest
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit04_timeperiod import TimePeriodValues, SimpleTimePeriod, TimePeriod


class MockTimePeriod(TimePeriod):
    """
    A generic time period implementation (not SimpleTimePeriod).
    Used to test the 'else' branch in _update_bounds.
    """
    def __init__(self, start_ts, end_ts):
        self._start = datetime.fromtimestamp(start_ts / 1000.0)
        self._end = datetime.fromtimestamp(end_ts / 1000.0)

    def get_start(self) -> datetime:
        return self._start

    def get_end(self) -> datetime:
        return self._end


class TestTimePeriodValuesRobust(unittest.TestCase):

    def test_max_middle_index_simple(self):
        """
        Original bug case: Verify max_middle_index.
        
        Java failure: Expected max_middle_index=1, got 3
        """
        s = TimePeriodValues("Test")
        s.add(SimpleTimePeriod(0, 100), 1.0)    # mid=50
        s.add(SimpleTimePeriod(100, 200), 2.0)  # mid=150
        s.add(SimpleTimePeriod(0, 50), 3.0)     # mid=25
        s.add(SimpleTimePeriod(50, 100), 4.0)   # mid=75
        
        # indices: 0(50), 1(150), 2(25), 3(75)
        # max middle is 150 at index 1
        self.assertEqual(s.get_max_middle_index(), 1, "Max middle index should be 1")

    def test_min_start_index(self):
        """Verify min_start_index."""
        s = TimePeriodValues("Test")
        s.add(SimpleTimePeriod(100, 200), 1.0)  # start=100 (idx 0)
        s.add(SimpleTimePeriod(50, 150), 2.0)   # start=50  (idx 1) -> Should be min
        s.add(SimpleTimePeriod(200, 300), 3.0)  # start=200 (idx 2)

        self.assertEqual(s.get_min_start_index(), 1, "Min start index should be 1 (start=50)")

    def test_max_start_index(self):
        """Verify max_start_index."""
        s = TimePeriodValues("Test")
        s.add(SimpleTimePeriod(100, 200), 1.0)
        s.add(SimpleTimePeriod(300, 400), 2.0)  # start=300 (idx 1) -> Should be max
        s.add(SimpleTimePeriod(200, 300), 3.0)

        self.assertEqual(s.get_max_start_index(), 1, "Max start index should be 1")

    def test_min_end_index(self):
        """Verify min_end_index."""
        s = TimePeriodValues("Test")
        s.add(SimpleTimePeriod(100, 200), 1.0)  # end=200
        s.add(SimpleTimePeriod(100, 150), 2.0)  # end=150 (idx 1) -> Should be min
        s.add(SimpleTimePeriod(100, 300), 3.0)  # end=300

        self.assertEqual(s.get_min_end_index(), 1, "Min end index should be 1")

    def test_max_end_index(self):
        """Verify max_end_index."""
        s = TimePeriodValues("Test")
        s.add(SimpleTimePeriod(100, 200), 1.0)
        s.add(SimpleTimePeriod(100, 400), 2.0)  # end=400 (idx 1) -> Should be max
        s.add(SimpleTimePeriod(100, 300), 3.0)

        self.assertEqual(s.get_max_end_index(), 1, "Max end index should be 1")

    def test_generic_time_period_support(self):
        """Test with MockTimePeriod to hit 'else' branches."""
        s = TimePeriodValues("Test Generic")
        # Add a mix of Simple and Mock
        s.add(MockTimePeriod(100, 200), 1.0)   # mid=150
        s.add(MockTimePeriod(300, 400), 2.0)   # mid=350 -> Max Middle
        s.add(SimpleTimePeriod(50, 100), 3.0)  # mid=75  -> Min Middle

        self.assertEqual(s.get_max_middle_index(), 1, "Max middle index (generic) should be 1")
        self.assertEqual(s.get_min_middle_index(), 2, "Min middle index (simple) should be 2")
        self.assertEqual(s.get_min_start_index(), 2, "Min start index should be 2 (start=50)")


if __name__ == "__main__":
    unittest.main()
