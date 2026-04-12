# -*- coding: utf-8 -*-
"""
Test for hit12_wordutils.py (WordUtils.abbreviate) - Complete Suite

"""

import os
import sys
import unittest


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit12_wordutils import WordUtils


class TestWordUtilsAbbreviate(unittest.TestCase):
    def test_abbreviate_lower_beyond_length(self):
        """
        Original bug case (Lang-45):
        Java equivalent: assertEquals("0123456789", WordUtils.abbreviate("0123456789", 15, 20, null));
        """
        result = WordUtils.abbreviate("0123456789", 15, 20, None)
        self.assertEqual("0123456789", result)

    def test_abbreviate_null_input(self):
        """Null input returns None."""
        self.assertIsNone(WordUtils.abbreviate(None, 1, -1, ""))

    def test_abbreviate_empty_string(self):
        """Empty string returns empty string."""
        self.assertEqual("", WordUtils.abbreviate("", 1, -1, ""))

    def test_abbreviate_no_limit(self):
        """upper = -1 means 'no limit'."""
        self.assertEqual("0123456789", WordUtils.abbreviate("0123456789", 0, -1, ""))


if __name__ == "__main__":
    unittest.main()

