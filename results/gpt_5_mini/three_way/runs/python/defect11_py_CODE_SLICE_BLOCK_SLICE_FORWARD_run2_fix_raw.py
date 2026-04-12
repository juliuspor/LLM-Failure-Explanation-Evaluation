@staticmethod
def random(count: int) -> str:
    return RandomStringUtils._random_internal(count, 0, 0, False, False, None, _RANDOM)