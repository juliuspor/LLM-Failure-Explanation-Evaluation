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

        if upper == -1 or upper > len(text):
            upper = len(text)
        if upper < lower:
            upper = lower

        # If lower is beyond the string length, we cannot find a space.
        # In that case, we should just return the whole string (or up to upper if upper is smaller).
        # But note: if lower > len(text), then substring_java(0, upper) would raise an error
        # because start (0) is fine, but end (upper) may be less than start? Actually upper is set to lower if lower > upper.
        # However, the main issue is that we might call substring_java with start > len(s) if lower > len(text) and we use lower as start.
        # But we never use lower as start; we only use 0 as start. So the only problematic case is when lower > len(text) and we call substring_java(0, upper) where upper = lower (since upper < lower condition) and lower > len(text).
        # Then substring_java(0, upper) with upper > len(s) will raise IndexError because end > len(s).
        # So we need to ensure that upper does not exceed len(text) after adjusting for lower.
        # Actually, we already set upper = len(text) if upper == -1 or upper > len(text). But if upper < lower, we set upper = lower.
        # So if lower > len(text), then upper becomes lower (which is > len(text)). Then substring_java(0, upper) will fail.
        # Therefore, we should cap upper at len(text) after the upper < lower adjustment.
        # Let's restructure: first, handle the case where lower > len(text). In that case, there is no space after lower, so we should return text up to upper (or whole text if upper is -1). But if lower > len(text), the string is shorter than lower, so we cannot abbreviate at a space after lower. The original Java code would return the substring from 0 to upper (with append if needed). However, if lower > len(text), the indexOf will return -1, and we go to the branch result = substring_java(text, 0, upper). But if upper is set to lower (because upper < lower) and lower > len(text), then upper > len(text) and substring_java will throw. So we need to ensure upper does not exceed len(text).
        # The fix: after adjusting upper for -1 and > len(text), then after the upper < lower adjustment, we should cap upper at len(text) again.
        # Alternatively, we can check if lower > len(text) and handle it early.
        # Let's adopt the early handling: if lower >= len(text), then there is no space after lower, so we can just return the whole string (or up to upper if upper is smaller). But we must still consider upper.
        # Actually, the Java implementation does not have this check; it would call indexOf with start index beyond length, which returns -1, then proceed to substring(0, upper). If upper is adjusted to lower (which is > length), substring throws StringIndexOutOfBoundsException. So the Java version also has a bug? Let's examine the original Java code (from Apache Commons Lang). I think the Java version does not have this bug because substring(0, upper) with upper > length throws. But the Java version likely ensures upper is not greater than length. Let's look at the Commons Lang 3.12.0 source: In WordUtils.abbreviate, they have:
        # if (upper == -1 || upper > str.length()) {
        #     upper = str.length();
        # }
        # if (upper < lower) {
        #     upper = lower;
        # }
        # Then they call str.indexOf(' ', lower). If lower > str.length(), indexOf returns -1. Then they do:
        # if (index == -1) {
        #     result = str.substring(0, upper);
        #     if (upper != str.length()) {
        #         result += appendToEnd;
        #     }
        # }
        # But if upper was set to lower (because upper < lower) and lower > str.length(), then upper > str.length(), and substring(0, upper) throws. So indeed there is a bug in the Java version as well? Wait, the condition upper < lower only sets upper = lower if upper < lower. If lower > str.length() and upper is -1, then upper becomes str.length() (since upper > str.length() is true). Then upper < lower? str.length() < lower, so yes, upper < lower, so upper = lower. Then upper > str.length(). So bug.
        # Therefore, we need to fix it. The fix is to ensure that after setting upper = lower, we still cap upper at len(text). Because if lower > len(text), the maximum we can go is len(text). So we should do: if upper > len(text): upper = len(text).
        # Let's implement that.
        # After adjusting upper for -1 and > len(text), and after upper < lower adjustment, we should cap upper at len(text).
        # But note: if upper is set to lower and lower > len(text), then upper > len(text). So we need to cap.
        # So add: if upper > len(text): upper = len(text)
        # However, we already set upper = len(text) if upper > len(text) earlier. But after upper = lower, it may become > len(text). So we need to re-check.
        # Let's restructure the upper adjustment:
        # 1. If upper == -1 or upper > len(text): upper = len(text)
        # 2. If upper < lower: upper = lower
        # 3. If upper > len(text): upper = len(text)   (this handles the case where lower > len(text))
        # Alternatively, we can combine: after step 2, set upper = min(upper, len(text)).
        # But note: if lower > len(text), then upper = lower > len(text), so min will bring it back to len(text). That's fine.
        # However, we must also consider that if lower > len(text), the indexOf will return -1, and we will return substring(0, upper) which is now substring(0, len(text)) i.e., the whole string. That seems correct: if the lower bound is beyond the string, we cannot abbreviate at a space, so we return the whole string (or up to upper if upper is smaller, but upper is len(text) so whole string). And we should not append append_to_end because upper == len(text). That matches the condition: if upper != len(text) then append.
        # So the fix is to add: upper = min(upper, len(text)) after the upper < lower adjustment.
        # But we don't have min imported; we can use built-in min.
        # Let's implement.

        # Step 1: adjust upper for -1 and out-of-range
        if upper == -1 or upper > len(text):
            upper = len(text)
        # Step 2: ensure upper is not less than lower
        if upper < lower:
            upper = lower
        # Step 3: ensure upper does not exceed string length (important when lower > len(text))
        if upper > len(text):
            upper = len(text)

        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            result = substring_java(text, 0, upper)
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)