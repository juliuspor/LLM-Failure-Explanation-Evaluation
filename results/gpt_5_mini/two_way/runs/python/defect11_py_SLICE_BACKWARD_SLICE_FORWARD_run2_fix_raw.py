@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if end <= start:
        raise ValueError(f"Invalid range: start ({start}) must be less than end ({end}).")
    gap = end - start
    if gap <= 0:
        raise ValueError(f"Invalid range gap: {gap}. start={start}, end={end}")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )