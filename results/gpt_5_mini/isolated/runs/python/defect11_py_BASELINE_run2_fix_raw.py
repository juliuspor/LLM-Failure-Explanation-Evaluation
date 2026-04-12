@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if end - start <= 0:
        raise ValueError(f"Invalid range: start={start}, end={end}; start must be less than end")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )