@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")
    # Derive defaults similar to _random_internal
    if start == 0 and end == 0:
        if letters or numbers:
            end = ord('z') + 1
            start = ord(' ')
        else:
            end = 127
            start = 0

    if start >= end:
        raise ValueError(f"Invalid range: start ({start}) must be less than end ({end})")

    gap = end - start

    # Build allowed character list based on filters to avoid infinite loops
    allowed: list[str] = []
    for cp in range(start, end):
        ch = chr(cp)
        if (letters and not ch.isalpha()):
            continue
        if (numbers and not ch.isdigit()):
            continue
        # skip private high surrogates
        if _is_private_high_surrogate(cp):
            continue
        allowed.append(ch)

    if not allowed:
        raise ValueError("No characters available in the given range that match the letters/numbers constraints")

    buffer: list[str] = [""] * count
    rnd = _RANDOM
    pos = count - 1

    while pos >= 0:
        ch = allowed[_next_int_java(rnd, len(allowed))]
        code_point = ord(ch)

        if _is_low_surrogate(code_point):
            if pos == 0:
                # cannot place low surrogate at the start; skip and retry
                continue
            buffer[pos] = ch
            pos -= 1
            # generate a high surrogate
            buffer[pos] = chr(55296 + _next_int_java(rnd, 128))
            pos -= 1
            continue

        if _is_high_surrogate(code_point):
            if pos == 0:
                continue
            # generate a low surrogate
            buffer[pos] = chr(56320 + _next_int_java(rnd, 128))
            pos -= 1
            buffer[pos] = ch
            pos -= 1
            continue

        buffer[pos] = ch
        pos -= 1

    return "".join(buffer)