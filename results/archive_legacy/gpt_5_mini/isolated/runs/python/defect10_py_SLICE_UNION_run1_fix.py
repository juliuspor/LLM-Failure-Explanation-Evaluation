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
    def char_at(s: str, index: int) -> str:
        if not isinstance(index, int):
            raise TypeError(f"index must be int, not {type(index).__name__}")
        if index < 0 or index >= len(s):
            raise IndexError(f"String index out of range: {index}")
        return s[index]
