    @staticmethod
    def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
        """
        Creates a random string based on a variety of options.
        """
        return RandomStringUtils._random_internal(count, start, end, letters, numbers, None, _RANDOM)

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
        """
        Internal worker that mirrors the upstream Java algorithm.
        """
        if count == 0:
            return ""
        if count < 0:
            raise ValueError(f"Requested random string length {count} is less than 0.")
        if chars is not None and len(chars) == 0:
            raise ValueError("The chars array must not be empty")

        # Derive a default character range.
        if start == 0 and end == 0:
            if chars is not None:
                end = len(chars)
            elif letters or numbers:
                end = ord("z") + 1
                start = ord(" ")
            else:
                # Simplified: stay in ASCII for stable/printable outputs.
                end = 127
                start = 0

        gap = end - start
        if gap <= 0:
            raise ValueError(f"start ({start}) must be less than end ({end}).")

        buffer: list[str] = [""] * count
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

        return "".join(buffer)