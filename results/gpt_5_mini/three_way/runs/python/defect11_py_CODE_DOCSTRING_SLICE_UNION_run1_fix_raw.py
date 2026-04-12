@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")
    # If both start and end are zero, defer to internal which derives defaults
    if not (start == 0 and end == 0):
        if end <= start:
            raise ValueError(f"Parameter end ({end}) must be greater than start ({start}).")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )