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
RandomStringUtils (Lang-11 / LANG-807) - random string generation utilities.

Buggy behavior: when explicit `start`/`end` bounds are provided and `end <= start`,
this implementation does not validate the parameters and instead fails later with a
Java-like lower-level message: "bound must be positive".
"""

from __future__ import annotations

import random

_RANDOM = random.Random(0)


class RandomStringUtils:
    @staticmethod
    def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
        if count == 0:
            return ""
        if count < 0:
            raise ValueError(f"Requested random string length {count} is less than 0.")

        if start == 0 and end == 0:
            if letters or numbers:
                end = ord("z") + 1
                start = ord(" ")
            else:
                end = 127
                start = 0

        if end <= start:
            raise ValueError(f"start ({start}) must be less than end ({end})")

        buffer: list[str] = []
        while len(buffer) < count:
            ch = chr(_RANDOM.randrange(start, end))
            if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
                buffer.append(ch)

        return "".join(buffer)