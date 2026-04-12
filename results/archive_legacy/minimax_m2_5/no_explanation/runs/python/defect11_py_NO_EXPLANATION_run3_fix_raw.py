@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if start == 0 and end == 0:
        if letters or numbers:
            start = ord(" ")
            end = ord("z") + 1
        else:
            start = 0
            end = 65536
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )