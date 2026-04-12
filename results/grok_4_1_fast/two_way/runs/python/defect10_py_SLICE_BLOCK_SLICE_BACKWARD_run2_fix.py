# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
NumberUtils (Lang-44) - Utility methods for Number parsing.


"""

import math
from decimal import Decimal, InvalidOperation
from typing import Optional, Union


def char_at(s: str, index: int) -> str:
    """
    Java-like String.charAt with bounds checks and a Java-style error message.
    """
    if index < 0 or index >= len(s):
        raise IndexError(f"String index out of range: {index}")
    return s[index]


class NumberUtils:
    """
    Utility methods for number parsing.
    """

    def __init__(self):
        """NumberUtils instances should NOT be constructed in standard programming."""
        pass

    # ----------------------------------------------------------------------
    # Simple conversions
    # ----------------------------------------------------------------------
    @staticmethod
    def string_to_int(val: Optional[str], default_value: int = 0) -> int:
        """
        Convert a string to an int, returning `default_value` if conversion fails.
        """
        try:
            if val is None:
                raise ValueError("None")
            return int(val, 10)
        except (ValueError, TypeError):
            return default_value

    # ----------------------------------------------------------------------
    # Predicates
    # ----------------------------------------------------------------------
    @staticmethod
    def is_digits(val: Optional[str]) -> bool:
        """
        Checks whether the string contains only digit characters.

        None and empty strings return False.
        """
        if val is None or len(val) == 0:
            return False
        for ch in val:
            if not ch.isdigit():
                return False
        return True

    @staticmethod
    def is_number(val: Optional[str]) -> bool:
        """
        Checks whether the string is a valid Java-style number.

        This mirrors the structure of the Java implementation (hex, exponent,
        decimal point, and type qualifiers).
        """
        if val is None or len(val) == 0:
            return False

        chars = list(val)
        sz = len(chars)
        has_exp = False
        has_dec_point = False
        allow_signs = False
        found_digit = False

        start = 1 if chars[0] == "-" else 0
        if sz > start + 1 and chars[start] == "0" and chars[start + 1] in ("x", "X"):
            # Hex
            i = start + 2
            if i == sz:
                return False
            while i < sz:
                c = chars[i]
                if not (
                    ("0" <= c <= "9")
                    or ("a" <= c <= "f")
                    or ("A" <= c <= "F")
                ):
                    return False
                i += 1
            return True

        sz -= 1  # don't want to loop to the last char, check it afterwards
        i = start
        while i < sz or (i < sz + 1 and allow_signs and not found_digit):
            c = chars[i]
            if "0" <= c <= "9":
                found_digit = True
                allow_signs = False
            elif c == ".":
                if has_dec_point or has_exp:
                    return False
                has_dec_point = True
            elif c in ("e", "E"):
                if has_exp or not found_digit:
                    return False
                has_exp = True
                allow_signs = True
            elif c in ("+", "-"):
                if not allow_signs:
                    return False
                allow_signs = False
                found_digit = False
            else:
                return False
            i += 1

        last_char = chars[-1]
        if "0" <= last_char <= "9":
            return True
        if last_char in ("e", "E"):
            return False
        if last_char in ("d", "D", "f", "F"):
            return found_digit
        if last_char in ("l", "L"):
            return found_digit and not has_exp and not has_dec_point
        return False

    # ----------------------------------------------------------------------
    # Factory helpers (small subset)
    # ----------------------------------------------------------------------
    @staticmethod
    def create_float(val: str) -> float:
        """Convert a string to a float."""
        return float(val)

    @staticmethod
    def create_double(val: str) -> float:
        """Convert a string to a double (float in Python)."""
        return float(val)

    @staticmethod
    def create_integer(val: str) -> int:
        """
        Convert a string to an integer, handling Java-like decode prefixes.

        Supports: `0x` / `-0x` / `+0x` hex, `#` hex, and leading-zero octal.
        """
        if len(val) == 0:
            raise ValueError("Empty string")

        sign = 1
        rest = val
        if rest[0] in ("-", "+"):
            sign = -1 if rest[0] == "-" else 1
            rest = rest[1:]

        base = 10
        if rest.startswith(("0x", "0X")):
            base = 16
            rest = rest[2:]
        elif rest.startswith("#"):
            base = 16
            rest = rest[1:]
        elif len(rest) > 1 and rest.startswith("0"):
            base = 8
            rest = rest[1:]

        if len(rest) == 0:
            raise ValueError(f"{val} is not a valid number.")

        return sign * int(rest, base)

    @staticmethod
    def create_long(val: str) -> int:
        """Convert a string to a long (int in Python)."""
        return int(val, 10)

    @staticmethod
    def create_big_integer(val: str) -> int:
        """Convert a string to a BigInteger (int in Python)."""
        return int(val, 10)

    @staticmethod
    def create_big_decimal(val: str) -> Decimal:
        """Convert a string to a BigDecimal (Decimal in Python)."""
        return Decimal(val)

    @staticmethod
    def _is_all_zeros(val: Optional[str]) -> bool:
        """
        Utility method for create_number.

        Returns True if `val` is None. Empty string returns False.
        """
        if val is None:
            return True
        for ch in reversed(val):
            if ch != "0":
                return False
        return len(val) > 0

    def char_at(s: str, index: int) -> str:
        """
        Java-like String.charAt with bounds checks and a Java-style error message.
        """
        if not (-len(s) <= index < len(s)):
            raise IndexError(f"String index out of range: {index}")
        return s[index]

    # ----------------------------------------------------------------------
    # Min/Max helpers (subset)
    # ----------------------------------------------------------------------
    @staticmethod
    def minimum(a: int, b: int, c: int) -> int:
        """Gets the minimum of three int values."""
        if b < a:
            a = b
        if c < a:
            a = c
        return a

    @staticmethod
    def maximum(a: int, b: int, c: int) -> int:
        """Gets the maximum of three int values."""
        if b > a:
            a = b
        if c > a:
            a = c
        return a