@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")
    # Validate and normalize start/end similar to _random_internal defaults
    if start == 0 and end == 0:
        # default range depends on letters/numbers; mirror logic from _random_internal
        if letters or numbers:
            end = ord('z') + 1
            start = ord(' ')
        else:
            end = 127
            start = 0
    if end <= start:
        raise ValueError(f"Range end ({end}) must be greater than start ({start}).")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )