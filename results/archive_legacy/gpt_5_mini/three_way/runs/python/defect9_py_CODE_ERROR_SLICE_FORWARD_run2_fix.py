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

from typing import List, Optional


class StringUtils:
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
        pairs = []
        for s, r in zip(search_list, replacement_list):
            if s is None or r is None:
                continue
            if len(s) == 0:
                continue
            pairs.append((s, r))
        if not pairs:
            return text
        search_length = len(pairs)
        no_more_matches_for_repl_index = [False] * search_length
        text_index = -1
        replace_index = -1
        for i, (s, r) in enumerate(pairs):
            temp_index = text.find(s)
            if temp_index == -1:
                no_more_matches_for_repl_index[i] = True
            elif text_index == -1 or temp_index < text_index:
                text_index = temp_index
                replace_index = i
        if text_index == -1:
            return text
        increase = 0
        for s, r in pairs:
            greater = len(r) - len(s)
            if greater > 0:
                increase += 3 * greater
        increase = min(increase, len(text) // 5)
        start = 0
        parts: List[str] = []
        while text_index != -1:
            parts.append(text[start:text_index])
            parts.append(pairs[replace_index][1])
            start = text_index + len(pairs[replace_index][0])
            text_index = -1
            replace_index = -1
            for i, (s, r) in enumerate(pairs):
                if no_more_matches_for_repl_index[i]:
                    continue
                temp_index = text.find(s, start)
                if temp_index == -1:
                    no_more_matches_for_repl_index[i] = True
                elif text_index == -1 or temp_index < text_index:
                    text_index = temp_index
                    replace_index = i
        parts.append(text[start:])
        return "".join(parts)
