@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if start < 0 or end < 0 or start >= end:
        raise ValueError(f"Invalid range: start={start}, end={end}")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )