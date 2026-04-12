@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")
    # Validate range to avoid passing non-positive bound to internal helper
    if start == 0 and end == 0:
        # delegate to internal which will derive defaults
        return RandomStringUtils._random_internal(
            count=count,
            start=start,
            end=end,
            letters=letters,
            numbers=numbers,
            chars=None,
            rnd=_RANDOM,
        )
    if end <= start:
        raise ValueError(f"Invalid range: end ({end}) must be greater than start ({start}).")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )