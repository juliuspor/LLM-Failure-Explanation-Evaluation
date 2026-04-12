@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if not isinstance(count, int):
        raise TypeError("count must be an int")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )