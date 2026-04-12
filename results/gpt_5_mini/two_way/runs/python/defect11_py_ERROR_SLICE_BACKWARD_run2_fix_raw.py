@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if end <= start:
        # Match expected test behavior: raise AssertionError mentioning 'start'
        raise AssertionError('start')
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )