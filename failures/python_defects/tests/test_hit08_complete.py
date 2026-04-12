# -*- coding: utf-8 -*-
"""
Test for hit08_locale.py (LocaleUtils.to_locale) - Complete Suite
Covers the language__variant format bug where empty country code handling is missing.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit08_locale import LocaleUtils, Locale


class TestLocaleUtilsToLocale(unittest.TestCase):
    
    def test_locale_with_empty_country_variant(self):
        """
        Original bug case: to_locale should handle language__variant format 
        (empty country with double underscore).
        
        Java equivalent: assertValidToLocale("fr__POSIX", "fr", "", "POSIX");
        
        Java failure: Invalid locale format because position 3 is '_' not uppercase letter
        """
        result = LocaleUtils.to_locale("fr__POSIX")
        expected = Locale("fr", "", "POSIX")
        self.assertEqual(result, expected)
    
    def test_locale_null_input(self):
        """Test that None input returns None."""
        result = LocaleUtils.to_locale(None)
        self.assertIsNone(result)
    
    def test_locale_language_only(self):
        """Test 2-character language only locale."""
        result = LocaleUtils.to_locale("en")
        expected = Locale("en", "")
        self.assertEqual(result, expected)
    
    def test_locale_language_country(self):
        """Test language_country format."""
        result = LocaleUtils.to_locale("en_US")
        expected = Locale("en", "US")
        self.assertEqual(result, expected)
    
    def test_locale_language_country_variant(self):
        """Test language_country_variant format."""
        result = LocaleUtils.to_locale("en_US_WIN")
        expected = Locale("en", "US", "WIN")
        self.assertEqual(result, expected)
    
    def test_locale_various_languages(self):
        """Test various language codes."""
        test_cases = [
            ("de", Locale("de", "")),
            ("fr", Locale("fr", "")),
            ("ja", Locale("ja", "")),
        ]
        for locale_str, expected in test_cases:
            with self.subTest(locale_str=locale_str):
                result = LocaleUtils.to_locale(locale_str)
                self.assertEqual(result, expected)
    
    def test_locale_various_countries(self):
        """Test various country codes."""
        test_cases = [
            ("de_DE", Locale("de", "DE")),
            ("fr_FR", Locale("fr", "FR")),
            ("ja_JP", Locale("ja", "JP")),
            ("zh_CN", Locale("zh", "CN")),
        ]
        for locale_str, expected in test_cases:
            with self.subTest(locale_str=locale_str):
                result = LocaleUtils.to_locale(locale_str)
                self.assertEqual(result, expected)
    
    def test_locale_empty_country_with_variant(self):
        """Test multiple cases of language__variant format."""
        test_cases = [
            ("en__UNIX", Locale("en", "", "UNIX")),
            ("de__DOS", Locale("de", "", "DOS")),
        ]
        for locale_str, expected in test_cases:
            with self.subTest(locale_str=locale_str):
                result = LocaleUtils.to_locale(locale_str)
                self.assertEqual(result, expected)
    
    def test_locale_invalid_length(self):
        """Test invalid locale format lengths."""
        invalid_cases = ["e", "eng", "e_US", "en_U"]
        for invalid in invalid_cases:
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    LocaleUtils.to_locale(invalid)
    
    def test_locale_invalid_language_case(self):
        """Test invalid language case (must be lowercase)."""
        invalid_cases = ["EN", "En", "EN_US"]
        for invalid in invalid_cases:
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    LocaleUtils.to_locale(invalid)
    
    def test_locale_invalid_country_case(self):
        """Test invalid country case (must be uppercase)."""
        invalid_cases = ["en_us", "en_Us"]
        for invalid in invalid_cases:
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    LocaleUtils.to_locale(invalid)
    
    def test_locale_invalid_separator(self):
        """Test invalid separator (must be underscore)."""
        invalid_cases = ["en-US", "en.US"]
        for invalid in invalid_cases:
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    LocaleUtils.to_locale(invalid)


if __name__ == "__main__":
    unittest.main()
