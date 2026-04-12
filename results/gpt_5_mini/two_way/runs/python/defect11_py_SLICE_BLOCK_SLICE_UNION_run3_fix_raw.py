@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")
    # Validate start/end range to avoid non-positive bounds passed to internal helper
    if start == 0 and end == 0:
        return RandomStringUtils._random_internal(count=count, start=start, end=end, letters=letters, numbers=numbers, chars=None, rnd=_RANDOM)
    if end <= start:
        raise ValueError(f"Parameter end ({end}) must be greater than start ({start}).")
    gap = end - start
    if gap <= 0:
        raise ValueError(f"Invalid character range: end ({end}) - start ({start}) = {gap}. Must be positive.")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )