@staticmethod
def random(count: int, start: int = 0, end: int = 0, letters: bool = False, numbers: bool = False) -> str:
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )