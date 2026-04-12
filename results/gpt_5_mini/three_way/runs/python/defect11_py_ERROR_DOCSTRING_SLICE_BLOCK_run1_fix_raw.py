@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if start is None or end is None:
        raise ValueError("start and end must be specified")
    bound = end - start
    if bound <= 0:
        raise ValueError(f"start must be less than end (start={start}, end={end})")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )