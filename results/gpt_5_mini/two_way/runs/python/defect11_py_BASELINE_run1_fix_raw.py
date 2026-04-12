@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if end - start <= 0:
        bound = end - start
        raise ValueError(f"start ({start}) and end ({end}) must define a positive bound: end - start = {bound}")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )