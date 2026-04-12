# -*- coding: utf-8 -*-
"""
Test for hit07_classutils.py (ClassUtils.to_class) - Complete Suite
Covers the null handling bug where None elements in array cause AttributeError.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit07_classutils import ClassUtils, ArrayUtils


class TestClassUtilsToClass(unittest.TestCase):
    
    def test_to_class_with_none_element(self):
        """
        Original bug case: to_class should handle arrays with None elements.
        
        Java equivalent:
        assertTrue(Arrays.equals(
            new Class[] { String.class, null, Double.class },
            ClassUtils.toClass(new Object[] { "Test", null, 99d })
        ));
        
        Java failure: NullPointerException when accessing null element
        """
        test_array = ["Test", None, 99.0]
        expected = [str, type(None), float]
        
        result = ClassUtils.to_class(test_array)
        self.assertEqual(result, expected)
    
    def test_to_class_null_input(self):
        """Test that None input returns None."""
        result = ClassUtils.to_class(None)
        self.assertIsNone(result)
    
    def test_to_class_empty_array(self):
        """Test that empty array returns empty array."""
        result = ClassUtils.to_class([])
        self.assertEqual(result, [])
    
    def test_to_class_all_strings(self):
        """Test with array of strings."""
        test_array = ["a", "b", "c"]
        result = ClassUtils.to_class(test_array)
        self.assertEqual(result, [str, str, str])
    
    def test_to_class_mixed_types(self):
        """Test with array of mixed types."""
        test_array = [1, 2.5, "hello", True]
        result = ClassUtils.to_class(test_array)
        self.assertEqual(result, [int, float, str, bool])
    
    def test_to_class_all_none(self):
        """Test with array of all None elements."""
        test_array = [None, None, None]
        result = ClassUtils.to_class(test_array)
        self.assertEqual(result, [type(None), type(None), type(None)])
    
    def test_to_class_single_element(self):
        """Test with single element array."""
        result = ClassUtils.to_class([42])
        self.assertEqual(result, [int])
    
    def test_to_class_single_none(self):
        """Test with single None element."""
        result = ClassUtils.to_class([None])
        self.assertEqual(result, [type(None)])
    
    def test_to_class_nested_list(self):
        """Test with nested lists."""
        test_array = [[1, 2], [3, 4]]
        result = ClassUtils.to_class(test_array)
        self.assertEqual(result, [list, list])


if __name__ == "__main__":
    unittest.main()
