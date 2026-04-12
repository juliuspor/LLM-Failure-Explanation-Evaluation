# -*- coding: utf-8 -*-
"""
Test for hit10_numberutils.py (NumberUtils.create_number) - Complete Suite

"""

import os
import sys
import unittest


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit10_numberutils import NumberUtils


class TestNumberUtilsCreateNumber(unittest.TestCase):
    def test_lang457_bad_inputs_raise_value_error(self):
        """
        Java equivalent (testLang457):
            String[] badInputs = new String[] { "l", "L", "f", "F", "junk", "bobL"};
            ...
            NumberFormatException was expected
        """
        bad_inputs = ["l", "L", "f", "F", "junk", "bobL"]
        for s in bad_inputs:
            with self.subTest(val=s):
                with self.assertRaises(ValueError):
                    NumberUtils.create_number(s)

    def test_create_number_numeric_string(self):
        """Sanity check: numeric strings parse."""
        self.assertEqual(123, NumberUtils.create_number("123"))


if __name__ == "__main__":
    unittest.main()

