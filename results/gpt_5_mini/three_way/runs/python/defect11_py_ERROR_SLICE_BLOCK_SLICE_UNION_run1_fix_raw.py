@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if start < 0:
        raise ValueError("start must be non-negative")
    if end <= start:
        raise ValueError("end must be greater than start")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )