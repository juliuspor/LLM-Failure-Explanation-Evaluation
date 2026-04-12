@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if start > end:
        raise ValueError(f"Invalid range: start ({start}) must not be greater than end ({end})")
    if start == end:
        raise ValueError(f"Invalid range: start ({start}) and end ({end}) must not be equal")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )