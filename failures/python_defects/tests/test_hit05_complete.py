# -*- coding: utf-8 -*-
"""
Test for hit05_arrayutils.py (ArrayUtils.add) - Complete Suite
Covers the LANG-35 bug: type inference when adding elements to arrays.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit05_arrayutils import ArrayUtils


class TestArrayUtilsAdd(unittest.TestCase):
    
    def test_add_null_to_null_with_expected_type(self):
        """
        Original bug case: ArrayUtils.add(null, null) returns Object[] but 
        caller expects String[]. Should handle type inference correctly.
        
        Java failure: java.lang.ClassCastException: [Ljava.lang.Object; 
                      cannot be cast to [Ljava.lang.String;
        """
        result = ArrayUtils.add(None, None, expected_type=str)
        self.assertEqual(result, [None], "Should return [None] without type error")
    
    def test_add_element_to_null_array(self):
        """Test adding a non-null element to a null array."""
        result = ArrayUtils.add(None, "hello")
        self.assertEqual(result, ["hello"])
        self.assertEqual(len(result), 1)
    
    def test_add_null_to_existing_array(self):
        """Test adding null element to an existing array."""
        arr = ["a", "b", "c"]
        result = ArrayUtils.add(arr, None)
        self.assertEqual(result, ["a", "b", "c", None])
        self.assertEqual(len(result), 4)
    
    def test_add_element_to_existing_array(self):
        """Test adding a regular element to an existing array."""
        arr = [1, 2, 3]
        result = ArrayUtils.add(arr, 4)
        self.assertEqual(result, [1, 2, 3, 4])
        # Original array should not be modified
        self.assertEqual(arr, [1, 2, 3])
    
    def test_add_to_empty_array(self):
        """Test adding an element to an empty array."""
        arr = []
        result = ArrayUtils.add(arr, "first")
        self.assertEqual(result, ["first"])
        self.assertEqual(len(result), 1)
    
    def test_add_preserves_order(self):
        """Test that elements are added at the end."""
        arr = ["x", "y"]
        result = ArrayUtils.add(arr, "z")
        self.assertEqual(result[-1], "z")
        self.assertEqual(result[0], "x")
        self.assertEqual(result[1], "y")
    
    def test_add_different_types(self):
        """Test adding elements of different types (Python is dynamically typed)."""
        arr = [1, "two", 3.0]
        result = ArrayUtils.add(arr, True)
        self.assertEqual(result, [1, "two", 3.0, True])
    
    def test_add_multiple_sequential(self):
        """Test multiple sequential additions."""
        arr = None
        arr = ArrayUtils.add(arr, "a")
        arr = ArrayUtils.add(arr, "b")
        arr = ArrayUtils.add(arr, "c")
        self.assertEqual(arr, ["a", "b", "c"])


class TestArrayUtilsAddAtIndex(unittest.TestCase):
    
    def test_add_at_index_beginning(self):
        """Test adding element at the beginning."""
        arr = [1, 2, 3]
        result = ArrayUtils.add_at_index(arr, 0, 0)
        self.assertEqual(result, [0, 1, 2, 3])
    
    def test_add_at_index_middle(self):
        """Test adding element in the middle."""
        arr = [1, 2, 3]
        result = ArrayUtils.add_at_index(arr, 1, 99)
        self.assertEqual(result, [1, 99, 2, 3])
    
    def test_add_at_index_end(self):
        """Test adding element at the end."""
        arr = [1, 2, 3]
        result = ArrayUtils.add_at_index(arr, 3, 4)
        self.assertEqual(result, [1, 2, 3, 4])
    
    def test_add_at_index_null_array(self):
        """Test adding to null array at index 0."""
        result = ArrayUtils.add_at_index(None, 0, "only")
        self.assertEqual(result, ["only"])
    
    def test_add_at_index_invalid_raises(self):
        """Test that invalid index raises error."""
        arr = [1, 2, 3]
        with self.assertRaises(IndexError):
            ArrayUtils.add_at_index(arr, 10, 99)
        with self.assertRaises(IndexError):
            ArrayUtils.add_at_index(arr, -1, 99)


if __name__ == "__main__":
    unittest.main()
