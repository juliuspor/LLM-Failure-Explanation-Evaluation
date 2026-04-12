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

from typing import Optional, Union


def char_at(s: str, index: int) -> str:
    """
    Java-like String.charAt with bounds checks and a Java-style error message.
    """
    if index < 0 or index >= len(s):
        raise IndexError(f"String index out of range: {index}")
    return s[index]


class NumberUtils:
    @staticmethod
    def create_number(val: Optional[str]) -> Optional[Union[int, float]]:
        if val is None:
            return None
        if len(val) == 0:
            raise ValueError('"" is not a valid number.')
        if val.startswith("--"):
            return None
        last_char = val[-1]
        if not last_char.isdigit():
            numeric = val[:-1]
            if last_char in ("l", "L"):
                if (numeric.startswith("-") and numeric[1:].isdigit()) or numeric.isdigit():
                    return int(numeric)
                raise ValueError(f"{val} is not a valid number.")
            raise ValueError(f"{val} is not a valid number.")
        if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
            return int(val)
        raise ValueError(f"{val} is not a valid number.")
