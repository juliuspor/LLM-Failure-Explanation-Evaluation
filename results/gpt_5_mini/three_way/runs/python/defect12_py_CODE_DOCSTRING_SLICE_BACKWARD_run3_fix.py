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
WordUtils (Lang-45) - Operations on strings that contain words.
"""

import os
from typing import Optional, Sequence


def substring_java(s: str, start: int, end: int) -> str:
    """
    Java-like substring(start, end) with bounds checks.

    Python slicing is safe; Java's String.substring throws if end > length.
    """
    if start < 0 or end < 0 or start > end or start > len(s) or end > len(s):
        raise IndexError(f"String index out of range: {end}")
    return s[start:end]


def _single_char(s: str, fallback: str) -> str:
    """
    Ensures we return a single character.

    Java's Character case conversions return a single `char`. Some Python string
    case conversions may expand (e.g., certain Unicode characters). For this
    translated code we keep the first character to stay "char-like".
    """
    if not s:
        return fallback
    return s[0]


def _to_title_char(ch: str) -> str:
    return _single_char(ch.title(), ch)


def _to_upper_char(ch: str) -> str:
    return _single_char(ch.upper(), ch)


def _to_lower_char(ch: str) -> str:
    return _single_char(ch.lower(), ch)


class SystemUtils:
    """Minimal subset used by WordUtils.wrap."""

    LINE_SEPARATOR = os.linesep


class StringUtils:
    EMPTY = ""

    @staticmethod
    def index_of(s: str, sub: str, start: int = 0) -> int:
        if s is None or sub is None:
            return -1
        if start < 0:
            start = 0
        idx = s.find(sub, start)
        return idx if idx != -1 else -1

    @staticmethod
    def default_string(s: Optional[str]) -> str:
        return "" if s is None else s


class WordUtils:
    """
    Operations on strings that contain words.

    This class tries to handle None input gracefully.
    An exception will not be thrown for a None input.
    """

    def __init__(self) -> None:
        """
        WordUtils instances should NOT be constructed in standard programming.
        Instead, the class should be used as WordUtils.wrap("foo bar", 20).

        This constructor is public to permit tools that require a JavaBean
        instance to operate.
        """
        super().__init__()

    # Wrapping
    # -----------------------------------------------------------------------
    @staticmethod
    def wrap(
        text: Optional[str],
        wrap_length: int,
        new_line_str: Optional[str] = None,
        wrap_long_words: bool = False,
    ) -> Optional[str]:
        """
        Wraps a single line of text, identifying words by ' '.

        Java equivalent: `WordUtils.wrap(String, int, String, boolean)`.

        Args:
            text: the string to be word wrapped, may be None
            wrap_length: the column to wrap the words at, less than 1 is treated as 1
            new_line_str: the string to insert for a new line; None uses system line separator
            wrap_long_words: True if long words (such as URLs) should be wrapped

        Returns:
            A line with newlines inserted, or None if text is None.
        """
        if text is None:
            return None
        if new_line_str is None:
            new_line_str = SystemUtils.LINE_SEPARATOR
        if wrap_length < 1:
            wrap_length = 1

        input_line_length = len(text)
        offset = 0
        wrapped_parts: list[str] = []

        while (input_line_length - offset) > wrap_length:
            if text[offset] == " ":
                offset += 1
                continue

            space_to_wrap_at = text.rfind(" ", 0, wrap_length + offset + 1)
            if space_to_wrap_at >= offset:
                wrapped_parts.append(text[offset:space_to_wrap_at])
                wrapped_parts.append(new_line_str)
                offset = space_to_wrap_at + 1
                continue

            if wrap_long_words:
                wrapped_parts.append(text[offset : wrap_length + offset])
                wrapped_parts.append(new_line_str)
                offset += wrap_length
                continue

            space_to_wrap_at = text.find(" ", wrap_length + offset)
            if space_to_wrap_at >= 0:
                wrapped_parts.append(text[offset:space_to_wrap_at])
                wrapped_parts.append(new_line_str)
                offset = space_to_wrap_at + 1
            else:
                wrapped_parts.append(text[offset:])
                offset = input_line_length

        wrapped_parts.append(text[offset:])
        return "".join(wrapped_parts)

    # Capitalizing
    # -----------------------------------------------------------------------
    @staticmethod
    def capitalize(text: Optional[str], delimiters: Optional[Sequence[str]] = None) -> Optional[str]:
        """
        Capitalizes all the delimiter separated words in a String.

        Java equivalent: `WordUtils.capitalize(String, char[])`.

        Args:
            text: the string to capitalize, may be None
            delimiters: set of characters to determine capitalization, None means whitespace

        Returns:
            Capitalized string, or None if text is None.
        """
        delim_len = -1 if delimiters is None else len(delimiters)
        if text is None or len(text) == 0 or delim_len == 0:
            return text

        buffer: list[str] = []
        capitalize_next = True
        for ch in text:
            if WordUtils._is_delimiter(ch, delimiters):
                buffer.append(ch)
                capitalize_next = True
            elif capitalize_next:
                buffer.append(_to_title_char(ch))
                capitalize_next = False
            else:
                buffer.append(ch)
        return "".join(buffer)

    @staticmethod
    def capitalize_fully(
        text: Optional[str], delimiters: Optional[Sequence[str]] = None
    ) -> Optional[str]:
        """
        Converts all the delimiter separated words in a String into capitalized words.

        Java equivalent: `WordUtils.capitalizeFully(String, char[])`.
        """
        delim_len = -1 if delimiters is None else len(delimiters)
        if text is None or len(text) == 0 or delim_len == 0:
            return text
        return WordUtils.capitalize(text.lower(), delimiters)

    @staticmethod
    def uncapitalize(text: Optional[str], delimiters: Optional[Sequence[str]] = None) -> Optional[str]:
        """
        Uncapitalizes all the delimiter separated words in a String.

        Java equivalent: `WordUtils.uncapitalize(String, char[])`.
        """
        delim_len = -1 if delimiters is None else len(delimiters)
        if text is None or len(text) == 0 or delim_len == 0:
            return text

        buffer: list[str] = []
        uncapitalize_next = True
        for ch in text:
            if WordUtils._is_delimiter(ch, delimiters):
                buffer.append(ch)
                uncapitalize_next = True
            elif uncapitalize_next:
                buffer.append(_to_lower_char(ch))
                uncapitalize_next = False
            else:
                buffer.append(ch)
        return "".join(buffer)

    @staticmethod
    def swap_case(text: Optional[str]) -> Optional[str]:
        """
        Swaps the case of a String using a word based algorithm.

        Java equivalent: `WordUtils.swapCase(String)`.
        """
        if text is None or len(text) == 0:
            return text

        buffer: list[str] = []
        whitespace = True

        for ch in text:
            if ch.isupper() or ch.istitle():
                tmp = _to_lower_char(ch)
            elif ch.islower():
                tmp = _to_title_char(ch) if whitespace else _to_upper_char(ch)
            else:
                tmp = ch

            buffer.append(tmp)
            whitespace = ch.isspace()

        return "".join(buffer)

    @staticmethod
    def initials(text: Optional[str], delimiters: Optional[Sequence[str]] = None) -> Optional[str]:
        """
        Extracts the initial letters from each word in the String.

        Java equivalent: `WordUtils.initials(String, char[])`.
        """
        if text is None or len(text) == 0:
            return text
        if delimiters is not None and len(delimiters) == 0:
            return ""

        buf: list[str] = []
        last_was_gap = True
        for ch in text:
            if WordUtils._is_delimiter(ch, delimiters):
                last_was_gap = True
            elif last_was_gap:
                buf.append(ch)
                last_was_gap = False
            else:
                pass
        return "".join(buf)

    @staticmethod
    def _is_delimiter(ch: str, delimiters: Optional[Sequence[str]]) -> bool:
        """Java equivalent: private static boolean isDelimiter(char, char[])."""
        if delimiters is None:
            return ch.isspace()
        for delim in delimiters:
            if ch == delim:
                return True
        return False

    @staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        text_len = len(text)
        if upper == -1 or upper > text_len:
            upper = text_len
        if upper < lower:
            upper = lower

        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            end = upper if upper <= text_len else text_len
            result = substring_java(text, 0, end)
            if upper != text_len:
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            end = upper if upper <= text_len else text_len
            return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

        end = index if index <= text_len else text_len
        return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)