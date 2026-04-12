@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")
    # If start and end specify a range, validate them
    if start >= end:
        raise ValueError(f"Invalid range: start ({start}) must be less than end ({end}).")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )