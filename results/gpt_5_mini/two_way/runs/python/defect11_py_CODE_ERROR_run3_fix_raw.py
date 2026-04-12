@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")
    # If a specific range is provided, ensure it's valid
    if start != 0 or end != 0:
        if start >= end:
            raise ValueError(f"start must be less than end: start={start}, end={end}")
        if start < 0:
            raise ValueError(f"start must be non-negative: start={start}")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )