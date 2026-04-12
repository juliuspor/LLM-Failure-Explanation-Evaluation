@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool, chars: Optional[Sequence[str]] = None) -> str:
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None if chars is None else list(chars),
        rnd=_RANDOM,
    )