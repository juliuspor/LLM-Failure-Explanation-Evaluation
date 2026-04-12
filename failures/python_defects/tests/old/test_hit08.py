# -*- coding: utf-8 -*-
"""
Test for hit08_locale.py (LocaleUtils.to_locale)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit08_locale import LocaleUtils, Locale


def test_locale_with_empty_country():
    """
    Test that to_locale handles language__variant format (empty country).
    
    Java equivalent:
    assertValidToLocale("fr__POSIX", "fr", "", "POSIX");
    """
    result = LocaleUtils.to_locale("fr__POSIX")
    expected = Locale("fr", "", "POSIX")
    assert result == expected, f"Expected {expected}, got {result}"


if __name__ == "__main__":
    try:
        test_locale_with_empty_country()
        print("Test passed!")
    except ValueError as e:
        print(f"Test failed with ValueError: {e}")
        sys.exit(1)
