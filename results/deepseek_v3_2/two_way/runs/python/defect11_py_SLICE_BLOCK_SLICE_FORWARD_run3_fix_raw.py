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

"""

from __future__ import annotations

import random
from typing import Optional, Sequence

_RANDOM = random.Random(0)


def _next_int_java(rnd: random.Random, bound: int) -> int:
    """
    Java-like `Random#nextInt(bound)` helper.

    Java throws `IllegalArgumentException("bound must be positive")` when
    `bound <= 0`. This helper preserves that error.
    """
    if bound <= 0:
        raise ValueError("bound must be positive")
    return rnd.randrange(bound)


def _is_low_surrogate(code_point: int) -> bool:
    # 0xDC00..0xDFFF
    return 56320 <= code_point <= 57343


def _is_high_surrogate(code_point: int) -> bool:
    # 0xD800..0xDB7F
    return 55296 <= code_point <= 56191


def _is_private_high_surrogate(code_point: int) -> bool:
    # 0xDB80..0xDBFF
    return 56192 <= code_point <= 56319


class RandomStringUtils:
    """
    Random string generation utilities.
    """

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def random_default(count: int) -> str:
        return RandomStringUtils.random_letters_numbers(count, letters=False, numbers=False)

    @staticmethod
    def random_ascii(count: int) -> str:
        return RandomStringUtils._random_internal(count, 32, 127, False, False, None, _RANDOM)

    @staticmethod
    def random_alphabetic(count: int) -> str:
        return RandomStringUtils.random_letters_numbers(count, letters=True, numbers=False)

    @staticmethod
    def random_alphanumeric(count: int) -> str:
        return RandomStringUtils.random_letters_numbers(count, letters=True, numbers=True)

    @staticmethod
    def random_numeric(count: int) -> str:
        return RandomStringUtils.random_letters_numbers(count, letters=False, numbers=True)

    @staticmethod
    def random_letters_numbers(count: int, letters: bool, numbers: bool) -> str:
        return RandomStringUtils._random_internal(count, 0, 0, letters, numbers, None, _RANDOM)

    @staticmethod
    def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
        return RandomStringUtils._random_internal(
            count=count,
            start=start,
            end=end,
            letters=letters,
            numbers=numbers,
            chars=None,
            rnd=_RANDOM,
        )

    @staticmethod
    def random_with_chars(
        count: int,
        start: int,
        end: int,
        letters: bool,
        numbers: bool,
        chars: Optional[Sequence[str]],
    ) -> str:
        return RandomStringUtils._random_internal(
            count=count,
            start=start,
            end=end,
            letters=letters,
            numbers=numbers,
            chars=None if chars is None else list(chars),
            rnd=_RANDOM,
        )

    @staticmethod
    def random_with_random_source(
        count: int,
        start: int,
        end: int,
        letters: bool,
        numbers: bool,
        chars: Optional[Sequence[str]],
        rnd: random.Random,
    ) -> str:
        return RandomStringUtils._random_internal(
            count=count,
            start=start,
            end=end,
            letters=letters,
            numbers=numbers,
            chars=None if chars is None else list(chars),
            rnd=rnd,
        )

    @staticmethod
    def random_from_string(count: int, chars: Optional[str]) -> str:
        if chars is None:
            return RandomStringUtils._random_internal(count, 0, 0, False, False, None, _RANDOM)
        return RandomStringUtils.random_from_chars(count, list(chars))

    @staticmethod
    def random_from_chars(count: int, chars: Optional[Sequence[str]]) -> str:
        if chars is None:
            return RandomStringUtils._random_internal(count, 0, 0, False, False, None, _RANDOM)
        return RandomStringUtils._random_internal(count, 0, len(chars), False, False, list(chars), _RANDOM)

    @staticmethod
    def _random_internal(
        count: int,
        start: int,
        end: int,
        letters: bool,
        numbers: bool,
        chars: Optional[Sequence[str]],
        rnd: random.Random,
    ) -> str:
        if count == 0:
            return ""
        if count < 0:
            raise ValueError(f"Requested random string length {count} is less than 0.")
        if chars is not None and len(chars) == 0:
            raise ValueError("The chars array must not be empty")

        if start == 0 and end == 0:
            if chars is not None:
                end = len(chars)
            elif letters or numbers:
                end = ord('z') + 1
                start = ord(' ')
            else:
                end = 127
                start = 0

        gap = end - start
        if gap <= 0:
            raise ValueError(f"Invalid range: start={start}, end={end}, gap={gap}")

        buffer = [''] * count
        pos = count - 1

        while pos >= 0:
            if chars is None:
                code_point = start + _next_int_java(rnd, gap)
                ch = chr(code_point)
            else:
                idx = start + _next_int_java(rnd, gap)
                ch = chars[idx]

            accepted = (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (
                not letters and not numbers
            )
            if not accepted:
                continue

            code_point = ord(ch)

            if _is_low_surrogate(code_point):
                if pos == 0:
                    continue
                buffer[pos] = ch
                pos -= 1
                buffer[pos] = chr(55296 + _next_int_java(rnd, 128))
                pos -= 1
                continue

            if _is_high_surrogate(code_point):
                if pos == 0:
                    continue
                buffer[pos] = chr(56320 + _next_int_java(rnd, 128))
                pos -= 1
                buffer[pos] = ch
                pos -= 1
                continue

            if _is_private_high_surrogate(code_point):
                continue

            buffer[pos] = ch
            pos -= 1

        return ''.join(buffer)