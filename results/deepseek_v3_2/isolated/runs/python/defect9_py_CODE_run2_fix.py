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

        # We'll work on a mutable list of characters (or just a string builder) but for simplicity, we can process sequentially.
        # The key is to apply replacements in order of appearance, but after each replacement, the string changes.
        # We'll use a while loop that scans from the current position, but we need to consider the updated string.
        # We'll keep a working string that we update as we go.
        working_text = text
        # We need to track the current position in the working_text, but we also need to find the earliest match among all search strings.
        # However, after a replacement, earlier positions may have changed, so we must restart scanning from the beginning of the working_text?
        # Actually, we can continue from the position after the replacement, but we must use the updated working_text.
        # The algorithm: while True:
        #   Find the earliest match among all search strings starting from current index.
        #   If no match, break.
        #   Perform replacement at that match.
        #   Update working_text and set current index to the position after the replacement.
        # However, we must also skip search strings that are empty or None, and replacements that are None.
        # We also need to avoid infinite loops if a replacement contains the search string (like typical replace).
        # The original algorithm intended to avoid re-checking already processed parts, but it used the original text.
        # We'll implement a new loop that uses the working_text.

        # Pre-process search and replacement pairs: filter out invalid ones.
        pairs = []
        for i in range(len(search_list)):
            search = search_list[i]
            replacement = replacement_list[i]
            if search is None or len(search) == 0 or replacement is None:
                # Skip this pair, as it won't be used.
                continue
            pairs.append((search, replacement))

        if not pairs:
            return working_text

        # We'll use a while loop that scans from the start of the working_text.
        # But we need to ensure we don't get stuck in an infinite loop if a replacement contains the search string.
        # The typical behavior of replace_each in Apache Commons Lang is to not re-scan the replaced part.
        # So we advance the start index after the replacement.
        start = 0
        # We'll build the result incrementally using a list of parts.
        parts = []
        # We need to find the earliest match among all pairs from start.
        while True:
            earliest_index = -1
            earliest_pair = None
            earliest_search_len = 0
            for search, replacement in pairs:
                # Find the first occurrence of search in working_text starting from start.
                index = working_text.find(search, start)
                if index != -1:
                    if earliest_index == -1 or index < earliest_index:
                        earliest_index = index
                        earliest_pair = (search, replacement)
                        earliest_search_len = len(search)
            if earliest_index == -1:
                # No more matches.
                parts.append(working_text[start:])
                break
            # Append the part before the match.
            parts.append(working_text[start:earliest_index])
            # Append the replacement.
            parts.append(earliest_pair[1])
            # Move start after the matched search string.
            start = earliest_index + earliest_search_len
        # Combine parts.
        return ''.join(parts)

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