@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count > 0 and end <= start:
        raise ValueError("Parameter 'end' must be greater than 'start'")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )