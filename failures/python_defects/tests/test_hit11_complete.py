# -*- coding: utf-8 -*-
"""
Test for hit11_randomstringutils.py (RandomStringUtils.random) - Complete Suite

"""

import os
import sys
import unittest


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hit11_randomstringutils import RandomStringUtils


class TestRandomStringUtilsRandom(unittest.TestCase):
    def test_lang807_message_mentions_start_and_end(self):
        """
        Original bug case (Lang-11 / LANG-807).

        Java equivalent:
            try {
                RandomStringUtils.random(3,5,5,false,false);
                fail("Expected IllegalArgumentException");
            } catch (IllegalArgumentException ex) {
                final String msg = ex.getMessage();
                assertTrue("Message (" + msg + ") must contain 'start'", msg.contains("start"));
                assertTrue("Message (" + msg + ") must contain 'end'", msg.contains("end"));
            }
        """
        try:
            RandomStringUtils.random(3, 5, 5, False, False)
            self.fail("Expected ValueError")
        except ValueError as ex:
            msg = str(ex)
            self.assertTrue("start" in msg, f"Message ({msg}) must contain 'start'")
            self.assertTrue("end" in msg, f"Message ({msg}) must contain 'end'")

    def test_random_zero_length_returns_empty(self):
        self.assertEqual("", RandomStringUtils.random(0, 0, 0, False, False))

    def test_random_returns_expected_length(self):
        result = RandomStringUtils.random(5, 0, 0, False, False)
        self.assertEqual(5, len(result))

    def test_random_negative_count_raises(self):
        with self.assertRaises(ValueError):
            RandomStringUtils.random(-1, 0, 0, False, False)


if __name__ == "__main__":
    unittest.main()
