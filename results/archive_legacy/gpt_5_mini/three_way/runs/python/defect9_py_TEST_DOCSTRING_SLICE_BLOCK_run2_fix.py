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

        search_length = len(search_list)
        no_more_matches_for_repl_index = [False] * search_length

        text_index = -1
        replace_index = -1

        for i in range(search_length):
            if (
                no_more_matches_for_repl_index[i]
                or search_list[i] is None
                or len(search_list[i]) == 0
                or replacement_list[i] is None
            ):
                continue
            temp_index = text.find(search_list[i])
            if temp_index == -1:
                no_more_matches_for_repl_index[i] = True
            elif text_index == -1 or temp_index < text_index:
                text_index = temp_index
                replace_index = i

        if text_index == -1:
            return text

        increase = 0

        for i in range(search_length):
            s_i = search_list[i]
            r_i = replacement_list[i]
            if s_i is None or r_i is None or len(s_i) == 0:
                continue
            greater = len(r_i) - len(s_i)
            if greater > 0:
                increase += 3 * greater
        increase = min(increase, len(text) // 5)

        start = 0
        parts: List[str] = []

        while text_index != -1:
            parts.append(text[start:text_index])
            parts.append(replacement_list[replace_index])

            start = text_index + len(search_list[replace_index])

            text_index = -1
            replace_index = -1

            for i in range(search_length):
                if (
                    no_more_matches_for_repl_index[i]
                    or search_list[i] is None
                    or len(search_list[i]) == 0
                    or replacement_list[i] is None
                ):
                    continue
                temp_index = text.find(search_list[i], start)
                if temp_index == -1:
                    no_more_matches_for_repl_index[i] = True
                elif text_index == -1 or temp_index < text_index:
                    text_index = temp_index
                    replace_index = i

        parts.append(text[start:])
        return "".join(parts)
