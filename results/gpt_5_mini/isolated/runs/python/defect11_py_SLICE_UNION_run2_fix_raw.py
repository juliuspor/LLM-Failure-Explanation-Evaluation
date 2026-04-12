@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")
    # Validate range
    if start == 0 and end == 0:
        # Delegate to internal which handles defaults
        from typing import Optional, Sequence
        return RandomStringUtils._random_internal(count, start, end, letters, numbers, None, _RANDOM)
    if end <= start:
        raise ValueError(f"Parameter end ({end}) must be greater than start ({start}).")
    # Ensure gap positive
    gap = end - start
    if gap <= 0:
        raise ValueError(f"Character range is empty: start={start}, end={end}.")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )