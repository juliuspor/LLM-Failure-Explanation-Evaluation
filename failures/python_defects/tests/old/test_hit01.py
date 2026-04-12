# -*- coding: utf-8 -*-
"""
Test for hit01_timezone.py (DateTimeZone.for_offset_hours_minutes)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit01_timezone import DateTimeZone


def test_negative_offset():
    """
    Test that for_offset_hours_minutes handles negative hour offsets correctly.
    
    Java equivalent:
    assertEquals(DateTimeZone.forID("-02:15"), DateTimeZone.forOffsetHoursMinutes(-2, -15));
    """
    zone = DateTimeZone.for_offset_hours_minutes(-2, -15)
    expected_id = "-02:15"
    assert zone.id == expected_id, f"Expected {expected_id}, got {zone.id}"
    
    zone2 = DateTimeZone.for_id("-02:15")
    assert zone == zone2


if __name__ == "__main__":
    try:
        test_negative_offset()
        print("Test passed!")
    except ValueError as e:
        print(f"Test failed with ValueError: {e}")
        sys.exit(1)
