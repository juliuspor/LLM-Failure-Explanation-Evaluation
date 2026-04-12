@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if start is None or end is None:
        raise ValueError("Both 'start' and 'end' must be provided and not None")
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("'start' and 'end' must be integers")
    if end <= start:
        raise ValueError(f"Invalid range: start ({start}) must be less than end ({end})")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )