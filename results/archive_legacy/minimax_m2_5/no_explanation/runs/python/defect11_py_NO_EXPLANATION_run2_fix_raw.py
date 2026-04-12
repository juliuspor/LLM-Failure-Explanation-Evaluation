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
            end = ord("z") + 1
            start = ord(" ")
        else:
            end = 127
            start = 0

    gap = end - start

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
            buffer[pos] = chr(55296 + _next_int_java(rnd, 1024))
            pos -= 1
            continue

        if _is_high_surrogate(code_point):
            if pos == 0:
                continue
            buffer[pos] = chr(56320 + _next_int_java(rnd, 1024))
            pos -= 1
            buffer[pos] = ch
            pos -= 1
            continue

        if _is_private_high_surrogate(code_point):
            continue

        buffer[pos] = ch
        pos -= 1

    return "".join(buffer)
