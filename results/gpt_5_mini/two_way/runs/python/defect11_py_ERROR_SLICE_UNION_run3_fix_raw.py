@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if start > 0 and end > 0 and end <= start:
        raise AssertionError(f"Invalid range: start ({start}) must be less than end ({end})")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )