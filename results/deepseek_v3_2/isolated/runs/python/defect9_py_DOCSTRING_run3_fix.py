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
StringUtils (Lang-39) - String replacement utilities.

"""

from typing import Iterable, List, Optional


class StringUtils:
    """
    Operations on strings that are None-safe.
    """

    EMPTY: str = ""
    INDEX_NOT_FOUND: int = -1
    PAD_LIMIT: int = 8192

    def __init__(self):
        """StringUtils instances should NOT be constructed in standard programming."""
        pass

    # ----------------------------------------------------------------------
    # Empty / blank checks
    # ----------------------------------------------------------------------
    @staticmethod
    def is_empty(seq: Optional[str]) -> bool:
        """Checks if a string is empty ("") or None."""
        return seq is None or len(seq) == 0

    @staticmethod
    def is_not_empty(seq: Optional[str]) -> bool:
        """Checks if a string is not empty ("") and not None."""
        return not StringUtils.is_empty(seq)

    @staticmethod
    def is_blank(seq: Optional[str]) -> bool:
        """Checks if a string is whitespace-only, empty, or None."""
        if seq is None:
            return True
        return seq.strip() == ""

    @staticmethod
    def is_not_blank(seq: Optional[str]) -> bool:
        """Checks if a string contains at least one non-whitespace character."""
        return not StringUtils.is_blank(seq)

    # ----------------------------------------------------------------------
    # Basic transforms
    # ----------------------------------------------------------------------
    @staticmethod
    def default_string(seq: Optional[str], default: str = EMPTY) -> str:
        """
        Returns either the passed in String, or the default if the input is None.
        """
        return default if seq is None else seq

    @staticmethod
    def trim(seq: Optional[str]) -> Optional[str]:
        """Trims whitespace from both ends of the string. None in -> None out."""
        if seq is None:
            return None
        return seq.strip()

    @staticmethod
    def strip(seq: Optional[str], strip_chars: Optional[str] = None) -> Optional[str]:
        """
        Strips whitespace (or the provided characters) from both ends of the string.

        Args:
            seq: input string, may be None
            strip_chars: characters to strip, or None to strip whitespace
        """
        if seq is None:
            return None
        if strip_chars is None:
            return seq.strip()
        return seq.strip(strip_chars)

    @staticmethod
    def strip_to_empty(seq: Optional[str]) -> str:
        """Strips a string, returning the empty string for None input."""
        stripped = StringUtils.strip(seq)
        return "" if stripped is None else stripped

    # ----------------------------------------------------------------------
    # Equality
    # ----------------------------------------------------------------------
    @staticmethod
    def equals(seq1: Optional[str], seq2: Optional[str]) -> bool:
        """Compares two strings, None-safe."""
        return seq1 == seq2

    @staticmethod
    def equals_ignore_case(seq1: Optional[str], seq2: Optional[str]) -> bool:
        """Compares two strings case-insensitively, None-safe."""
        if seq1 is None or seq2 is None:
            return seq1 is seq2
        return seq1.lower() == seq2.lower()

    # ----------------------------------------------------------------------
    # Searching
    # ----------------------------------------------------------------------
    @staticmethod
    def index_of(seq: Optional[str], search_seq: Optional[str], start_pos: int = 0) -> int:
        """Returns the first index of `search_seq` in `seq`, or -1 if not found/invalid."""
        if seq is None or search_seq is None:
            return StringUtils.INDEX_NOT_FOUND
        return seq.find(search_seq, max(start_pos, 0))

    @staticmethod
    def contains(seq: Optional[str], search_seq: Optional[str]) -> bool:
        """Checks if `seq` contains `search_seq`, None-safe."""
        return StringUtils.index_of(seq, search_seq) != StringUtils.INDEX_NOT_FOUND

    # ----------------------------------------------------------------------
    # Replace (single search string)
    # ----------------------------------------------------------------------
    @staticmethod
    def replace_once(text: Optional[str], search_string: Optional[str], replacement: Optional[str]) -> Optional[str]:
        """Replaces the first occurrence of `search_string` within `text`."""
        return StringUtils.replace_max(text, search_string, replacement, 1)

    @staticmethod
    def replace(text: Optional[str], search_string: Optional[str], replacement: Optional[str]) -> Optional[str]:
        """Replaces all occurrences of `search_string` within `text`."""
        return StringUtils.replace_max(text, search_string, replacement, -1)

    @staticmethod
    def replace_max(
        text: Optional[str],
        search_string: Optional[str],
        replacement: Optional[str],
        max_replacements: int,
    ) -> Optional[str]:
        """
        Replaces up to `max_replacements` occurrences of `search_string` within `text`.

        This follows the structure of the Java implementation (replace with max).
        """
        if text is None or StringUtils.is_empty(search_string) or replacement is None or max_replacements == 0:
            return text

        start = 0
        end = text.find(search_string, start)
        if end == -1:
            return text

        repl_length = len(search_string)
        increase = len(replacement) - repl_length
        increase = 0 if increase < 0 else increase
        if max_replacements < 0:
            increase *= 16
        else:
            increase *= min(max_replacements, 64)

        parts: List[str] = []
        while end != -1:
            parts.append(text[start:end])
            parts.append(replacement)
            start = end + repl_length
            if max_replacements > 0:
                max_replacements -= 1
                if max_replacements == 0:
                    break
            end = text.find(search_string, start)

        parts.append(text[start:])
        return "".join(parts)

    # ----------------------------------------------------------------------
    # Misc
    # ----------------------------------------------------------------------
    @staticmethod
    def repeat(seq: Optional[str], repeat: int) -> Optional[str]:
        """Repeats a string `repeat` times. None in -> None out."""
        if seq is None:
            return None
        if repeat <= 0:
            return ""
        return seq * repeat

    @staticmethod
    def replace_each(
        text: Optional[str],
        search_list: Optional[List[Optional[str]]],
        replacement_list: Optional[List[Optional[str]]],
    ) -> Optional[str]:
        if text is None:
            return None
        if text == "":
            return ""
        if search_list is None or replacement_list is None:
            return text
        if len(search_list) == 0 or len(replacement_list) == 0:
            return text
        if len(search_list) != len(replacement_list):
            raise ValueError(
                f"Search and Replace array lengths don't match: {len(search_list)} vs {len(replacement_list)}"
            )

        # Work on mutable copy of text
        result = text
        # We'll process replacements in a loop, scanning from left to right.
        # We need to consider that after a replacement, the new text may have new matches
        # for the same or other search strings that start before the replacement end.
        # The standard algorithm used in Apache Commons Lang (Java) uses a while loop
        # that finds the earliest match among all search strings at each iteration.
        # However, after replacing, it continues searching from the start of the replacement,
        # not from the beginning of the replaced substring. This can miss overlaps.
        # The fix is to restart scanning from the beginning of the replaced substring
        # (i.e., the index where the match started) plus the length of the replacement,
        # but we must also consider that the replacement may contain search strings.
        # Actually, the Java implementation does not restart from the beginning; it continues
        # from after the replacement. Overlaps are not supported. The bug is that the
        # algorithm does not account for the fact that the replacement may have changed
        # the text, so subsequent find operations on the original text are invalid.
        # We need to update the text after each replacement and search again from the
        # position after the replacement.
        # However, the original code uses `text.find` on the original text, which is wrong.
        # We must update `text` (or a mutable copy) after each replacement.
        # Let's implement the correct algorithm:
        # 1. Create a mutable string (we'll use a list of characters or just rebuild string each time).
        # 2. Iterate over the text index from 0.
        # 3. For each position, check each search string to see if it matches at that position.
        # 4. If a match is found, replace it, and move the index to after the replacement.
        # 5. Continue until the end of the string.
        # This is similar to the algorithm used in Apache Commons Lang's replaceEach.
        # However, the original Java implementation uses a while loop that finds the earliest
        # match among all search strings, then replaces, then continues from after the replacement.
        # It does not restart from the beginning of the replaced substring. Overlaps are not handled.
        # The bug in the provided code is that it uses the original `text` for all find operations,
        # ignoring replacements. So we need to update the text after each replacement.
        # Let's fix by building the result incrementally, similar to the original but updating the text.
        # We'll keep a buffer (list of parts) and a current position, but we need to search in the
        # remaining original text? Actually, we need to search in the original text for matches that
        # start at or after the current position, but after a replacement, the original indices shift.
        # The simplest fix is to use a while loop that searches in the original text, but after each
        # replacement, we adjust the start position by the difference in length between the search
        # and replacement strings. However, this is complex because the text changes.
        # Better to rebuild the string step by step, searching in the remaining original substring.
        # We'll keep a variable `current_text` that is the remaining part of the original text that
        # hasn't been processed yet. When we find a match, we append the part before the match and
        # the replacement to the result, and then set `current_text` to the part after the match.
        # Then we continue searching in `current_text`. This way, we don't need to adjust indices.
        # However, we must also consider that matches may overlap across the boundary? No, because
        # we cut off the matched part. Overlaps within the same segment are handled because we
        # always search from the start of `current_text`.
        # Let's implement:
        result_parts = []
        current_text = text
        while True:
            # Find the earliest match among all search strings in current_text
            earliest_index = -1
            replace_idx = -1
            for i in range(search_length):
                search = search_list[i]
                if search is None or len(search) == 0 or replacement_list[i] is None:
                    continue
                pos = current_text.find(search)
                if pos != -1 and (earliest_index == -1 or pos < earliest_index):
                    earliest_index = pos
                    replace_idx = i
            if earliest_index == -1:
                # No more matches
                result_parts.append(current_text)
                break
            # Append the part before the match
            result_parts.append(current_text[:earliest_index])
            # Append the replacement
            result_parts.append(replacement_list[replace_idx])
            # Update current_text to the part after the match
            current_text = current_text[earliest_index + len(search_list[replace_idx]):]
        return "".join(result_parts)

    @staticmethod
    def join(parts: Optional[Iterable[Optional[str]]], separator: str = "") -> Optional[str]:
        """
        Joins elements into a single string, treating None inputs as None.

        This mirrors the style of other Lang utilities where None inputs are
        handled gracefully.
        """
        if parts is None:
            return None
        out: List[str] = []
        for item in parts:
            if item is not None:
                out.append(item)
        return separator.join(out)