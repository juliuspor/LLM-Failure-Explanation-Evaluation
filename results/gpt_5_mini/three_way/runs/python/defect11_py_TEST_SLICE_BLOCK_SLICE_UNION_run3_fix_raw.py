@staticmethod
def random(count: int, start: int = 0, end: int = 0, letters: bool = False, numbers: bool = False, chars: Optional[Sequence[str]] = None, rnd: Optional[random.Random] = None) -> str:
    if rnd is None:
        rnd = _RANDOM
    # If chars is a string, convert to list of single-character strings
    if isinstance(chars, str):
        chars = list(chars)
    return RandomStringUtils._random_internal(count=count, start=start, end=end, letters=letters, numbers=numbers, chars=None if chars is None else list(chars), rnd=rnd)