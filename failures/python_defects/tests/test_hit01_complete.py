# -*- coding: utf-8 -*-
"""
Test for hit01_timezone.py (DateTimeZone.for_offset_hours_minutes) - Complete Suite
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit01_timezone import DateTimeZone, DateTimeConstants

class TestDateTimeZone(unittest.TestCase):

    def test_zero_offset(self):
        """Test that (0, 0) returns UTC."""
        zone = DateTimeZone.for_offset_hours_minutes(0, 0)
        self.assertEqual(zone, DateTimeZone.UTC)
        self.assertEqual(zone.get_id(), "UTC")
        self.assertEqual(zone.get_offset(0), 0)

    def test_positive_hours_minutes(self):
        """Test standard positive offsets: (2, 15) -> +02:15."""
        zone = DateTimeZone.for_offset_hours_minutes(2, 15)
        # 2 * 3600000 + 15 * 60000 = 7200000 + 900000 = 8100000
        expected_millis = 2 * 3600000 + 15 * 60000
        self.assertEqual(zone.get_offset(0), expected_millis)
        self.assertEqual(zone.get_id(), "+02:15")

    def test_positive_hours_zero_minutes(self):
        """Test positive hours with zero minutes: (2, 0) -> +02:00."""
        zone = DateTimeZone.for_offset_hours_minutes(2, 0)
        expected_millis = 2 * 3600000
        self.assertEqual(zone.get_offset(0), expected_millis)
        self.assertEqual(zone.get_id(), "+02:00")
        
    def test_negative_hours_zero_minutes(self):
        """Test negative hours with zero minutes: (-2, 0) -> -02:00."""
        zone = DateTimeZone.for_offset_hours_minutes(-2, 0)
        expected_millis = -2 * 3600000
        self.assertEqual(zone.get_offset(0), expected_millis)
        self.assertEqual(zone.get_id(), "-02:00")

    def test_negative_hours_negative_minutes(self):
        """
        Test that both negative inputs result in negative total offset.
        (-2, -15) -> -02:15
        This matches Joda-Time behavior where signs usually match or are handled cumulatively.
        Reference failure case: assertEquals(DateTimeZone.forID("-02:15"), DateTimeZone.forOffsetHoursMinutes(-2, -15));
        """
        zone = DateTimeZone.for_offset_hours_minutes(-2, -15)
        # -2h - 15m = -(2h + 15m) = -8100000
        expected_millis = -(2 * 3600000 + 15 * 60000)
        self.assertEqual(zone.get_offset(0), expected_millis, "Offset should be sum of negative parts")
        self.assertEqual(zone.get_id(), "-02:15")

    def test_zero_hours_positive_minutes(self):
        """Test (0, 15) -> +00:15."""
        zone = DateTimeZone.for_offset_hours_minutes(0, 15)
        expected_millis = 15 * 60000
        self.assertEqual(zone.get_offset(0), expected_millis)
        self.assertEqual(zone.get_id(), "+00:15")

    def test_zero_hours_negative_minutes(self):
        """Test (0, -15) -> -00:15."""
        zone = DateTimeZone.for_offset_hours_minutes(0, -15)
        expected_millis = -15 * 60000
        self.assertEqual(zone.get_offset(0), expected_millis)
        self.assertEqual(zone.get_id(), "-00:15")

    def test_boundaries(self):
        """Test edge cases for hours and minutes."""
        # Max hours +23
        zone = DateTimeZone.for_offset_hours_minutes(23, 59)
        self.assertEqual(zone.get_id(), "+23:59")
        
        # Min hours -23
        zone = DateTimeZone.for_offset_hours_minutes(-23, -59)
        self.assertEqual(zone.get_id(), "-23:59")

    def test_mixed_signs_invalid(self):
        """
        According to Joda-Time docs (and logical inference from the prompt):
        Minutes must be negative if hours are negative?
        Actually, Joda-Time forOffsetHoursMinutes says:
        'The minutes value must be in the range -59 to +59.'
        And 'The following combinations of sign for the hour and minute are possible:'
        +ve, +ve -> OK
        +ve, -ve -> Error
        -ve, +ve -> Error (Wait, or just -ve?)
        
        Let's look at the docstring in hit01_timezone.py again (lines 363-378).
        > +ve, -ve -> ValueError
        > -ve, +ve -> -02:15 (wait, doc says -02:15 for (-2, 15)???)
        
        Let's re-read the docstring carefully.
        
        Lines 375: -ve     +ve       (-2, 15)   -02:15
        Lines 377: -ve     -ve       (-2, -15)  -02:15
        
        This implies that for negative hours, the minutes are treated as extending the magnitude of the offset, regardless of sign? 
        Or that (-2, 15) and (-2, -15) both produce -02:15?
        
        If (-2, 15) produces -02:15, that means the method calculates -2h - 15m.
        If (-2, -15) produces -02:15, that means the method calculates -2h - 15m.
        
        The standard behavior (usually) is strict checking or additive.
        However, the docstring in the file explicitly lists the expected behavior.
        I will test ACCORDING TO THE DOCSTRING format provided in the file to be safe.
        
        Docstring says:
        (-2, 15) -> -02:15
        (-2, -15) -> -02:15
        
        ((2, -15)) -> ValueError
        
        I will verify (-2, 15) works too.
        """
        # (-2, 15) -> -02:15
        zone = DateTimeZone.for_offset_hours_minutes(-2, 15)
        self.assertEqual(zone.get_id(), "-02:15")
        
        # (2, -15) -> ValueError
        with self.assertRaises(ValueError):
            DateTimeZone.for_offset_hours_minutes(2, -15)

    def test_out_of_range(self):
        """Test values outside accepted ranges."""
        # Hours > 23
        with self.assertRaises(ValueError):
            DateTimeZone.for_offset_hours_minutes(24, 0)
        
        # Hours < -23
        with self.assertRaises(ValueError):
            DateTimeZone.for_offset_hours_minutes(-24, 0)
            
        # Minutes > 59
        with self.assertRaises(ValueError):
            DateTimeZone.for_offset_hours_minutes(2, 60)
            
        # Minutes < -59
        with self.assertRaises(ValueError):
            DateTimeZone.for_offset_hours_minutes(-2, -60)


if __name__ == "__main__":
    unittest.main()
