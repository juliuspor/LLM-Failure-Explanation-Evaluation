@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count < 0:
        raise ValueError(f"count must be non-negative: {count}")
    if start >= end:
        raise ValueError(f"start must be less than end: start={start}, end={end}")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )