# -*- coding: utf-8 -*-
"""
Test for hit09_stringutils.py (StringUtils.replace_each) - Complete Suite

"""

import os
import sys
import unittest


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit09_stringutils import StringUtils


class TestStringUtilsReplaceEach(unittest.TestCase):
    def test_null_safety_inside_arrays_single(self):
        """
        Java equivalent:
          assertEquals(StringUtils.replaceEach("aba", new String[]{"a"}, new String[]{null}),"aba");
        """
        result = StringUtils.replace_each("aba", ["a"], [None])
        self.assertEqual("aba", result)

    def test_null_safety_inside_arrays_mixed(self):
        """
        Original bug case (Lang-39):
          assertEquals(StringUtils.replaceEach("aba", new String[]{"a", "b"}, new String[]{"c", null}),"cbc");
        """
        result = StringUtils.replace_each("aba", ["a", "b"], ["c", None])
        self.assertEqual("cbc", result)

    def test_replace_each_basic(self):
        """Sanity check (non-null inputs)."""
        result = StringUtils.replace_each("abcde", ["ab", "d"], ["w", "t"])
        self.assertEqual("wcte", result)


if __name__ == "__main__":
    unittest.main()

