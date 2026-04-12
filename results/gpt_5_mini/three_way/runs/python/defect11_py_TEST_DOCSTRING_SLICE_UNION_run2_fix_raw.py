@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if end <= start:
        raise ValueError(f"Parameter end ({end}) must be greater than start ({start})")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )