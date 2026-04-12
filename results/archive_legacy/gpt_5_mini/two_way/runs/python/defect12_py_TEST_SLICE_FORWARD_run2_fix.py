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

from typing import Optional


def substring_java(s: str, start: int, end: int) -> str:
    """
    Java-like substring(start, end) with bounds checks.

    Python slicing is safe; Java's String.substring throws if end > length.
    """
    if start < 0 or end < 0 or start > end or start > len(s) or end > len(s):
        raise IndexError(f"String index out of range: {end}")
    return s[start:end]


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
    @staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY
        if lower >= len(text):
            return text
        upper_limit = None
        if upper == -1:
            upper_limit = None
        else:
            if upper > len(text):
                upper = len(text)
            if upper < lower:
                upper = lower
            upper_limit = upper
        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            if upper_limit is None:
                return text
            result = substring_java(text, 0, upper_limit)
            if upper_limit != len(text):
                result += StringUtils.default_string(append_to_end)
            return result
        if upper_limit is None:
            return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)
        if index > upper_limit:
            return substring_java(text, 0, upper_limit) + StringUtils.default_string(append_to_end)
        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)