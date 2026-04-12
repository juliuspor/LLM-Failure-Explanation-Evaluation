@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if end <= start:
        # Ensure a positive range; make end just above start so _random_internal's gap > 0
        end = start + 1
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )