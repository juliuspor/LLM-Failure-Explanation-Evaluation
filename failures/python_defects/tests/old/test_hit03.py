# -*- coding: utf-8 -*-
"""
Test for hit03_translator.py (CharSequenceTranslator.translate)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit03_translator import CsvEscaper


def test_translate_surrogate_pair():
    """
    Test that translate handles surrogate pairs (emoji) correctly.
    
    Java equivalent:
    assertEquals("\uD83D\uDE30", StringEscapeUtils.escapeCsv("\uD83D\uDE30"));
    
    \uD83D\uDE30 is the surrogate pair for U+1F630 (😰)
    """
    escaper = CsvEscaper()
    input_str = "\U0001F630"  # Emoji character (same as Java's \uD83D\uDE30)
    result = escaper.translate_string(input_str)
    expected = "\U0001F630"
    assert result == expected, f"Expected {expected!r}, got {result!r}"


if __name__ == "__main__":
    try:
        test_translate_surrogate_pair()
        print("Test passed!")
    except IndexError as e:
        print(f"Test failed with IndexError: {e}")
        sys.exit(1)
