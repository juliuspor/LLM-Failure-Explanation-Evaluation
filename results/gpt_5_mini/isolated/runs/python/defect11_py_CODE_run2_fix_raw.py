@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    return RandomStringUtils._random_internal(count, start, end, letters, numbers, None, _RANDOM)
