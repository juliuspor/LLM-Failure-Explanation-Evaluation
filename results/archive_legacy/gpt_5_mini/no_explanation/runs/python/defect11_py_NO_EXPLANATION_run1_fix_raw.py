@staticmethod
def random(count: int, start: int = 0, end: int = 0, letters: bool = False, numbers: bool = False, chars: Optional[Sequence[str]] = None, rnd: Optional[random.Random] = None) -> str:
    if rnd is None:
        rnd = _RANDOM
    # Normalize chars to list if provided
    char_list = None if chars is None else list(chars)
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=char_list,
        rnd=rnd,
    )