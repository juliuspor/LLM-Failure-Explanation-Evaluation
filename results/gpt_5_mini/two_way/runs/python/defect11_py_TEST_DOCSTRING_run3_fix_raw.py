@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if start >= end:
        raise ValueError(f"start ({start}) must be less than end ({end})")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )