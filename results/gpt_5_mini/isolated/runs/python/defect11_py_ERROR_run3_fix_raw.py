@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if start == 0 and end == 0:
        # Delegate to internal which derives sensible defaults
        return RandomStringUtils._random_internal(
            count=count,
            start=0,
            end=0,
            letters=letters,
            numbers=numbers,
            chars=None,
            rnd=_RANDOM,
        )
    if end <= start:
        raise ValueError(f"Parameter 'end' ({end}) must be greater than 'start' ({start}).")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )