# -*- coding: utf-8 -*-
"""
Test for hit03_translator.py (CharSequenceTranslator.translate) - Complete Suite
Covers the surrogate pair handling bug where index advances incorrectly.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit03_translator import CsvEscaper, to_utf16_code_units, code_point_at


class TestCharSequenceTranslator(unittest.TestCase):
    
    def test_translate_surrogate_pair_with_suffix(self):
        """
        Original bug case: translate should handle surrogate pairs followed by another character.
        
        Java equivalent: Translating emoji followed by a character should preserve both.
        
        Java failure: IndexError when advancing past surrogate pair
        """
        escaper = CsvEscaper()
        # \U0001F630 is a surrogate pair in UTF-16 (😰)
        input_str = "\U0001F630A"
        result = escaper.translate_string(input_str)
        expected = "\U0001F630A"
        
        self.assertEqual(result, expected, f"Expected {expected!r}, got {result!r}")
    
    def test_translate_single_surrogate_pair(self):
        """Test translating a single emoji (surrogate pair)."""
        escaper = CsvEscaper()
        input_str = "\U0001F600"  # 😀
        result = escaper.translate_string(input_str)
        self.assertEqual(result, input_str)
    
    def test_translate_ascii_only(self):
        """Test translating ASCII-only string."""
        escaper = CsvEscaper()
        input_str = "Hello, World!"
        result = escaper.translate_string(input_str)
        self.assertEqual(result, input_str)
    
    def test_translate_empty_string(self):
        """Test translating empty string."""
        escaper = CsvEscaper()
        result = escaper.translate_string("")
        self.assertEqual(result, "")
    
    def test_translate_multiple_surrogates(self):
        """Test translating multiple emoji characters."""
        escaper = CsvEscaper()
        input_str = "\U0001F600\U0001F601\U0001F602"  # 😀😁😂
        result = escaper.translate_string(input_str)
        self.assertEqual(result, input_str)
    
    def test_translate_mixed_content(self):
        """Test translating mixed ASCII and emoji."""
        escaper = CsvEscaper()
        input_str = "Hello \U0001F600 World"
        result = escaper.translate_string(input_str)
        self.assertEqual(result, input_str)
    
    def test_translate_surrogate_at_end(self):
        """Test surrogate pair at the end of string."""
        escaper = CsvEscaper()
        input_str = "Test\U0001F600"
        result = escaper.translate_string(input_str)
        self.assertEqual(result, input_str)


if __name__ == "__main__":
    unittest.main()
