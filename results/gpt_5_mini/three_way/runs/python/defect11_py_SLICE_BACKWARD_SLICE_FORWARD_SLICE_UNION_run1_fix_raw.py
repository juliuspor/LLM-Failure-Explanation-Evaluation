@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    # Validate count
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")

    # Normalize start/end: follow _random_internal behavior where start==end==0 means defaults
    if start == 0 and end == 0:
        return RandomStringUtils._random_internal(count=count, start=start, end=end, letters=letters, numbers=numbers, chars=None, rnd=_RANDOM)

    # Ensure start <= end
    if end < start:
        raise ValueError(f"Start ({start}) must not be greater than end ({end}).")

    # If range is empty (gap == 0), adjust to allow single choice: treat as a single value range
    if end == start:
        end = start + 1

    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )