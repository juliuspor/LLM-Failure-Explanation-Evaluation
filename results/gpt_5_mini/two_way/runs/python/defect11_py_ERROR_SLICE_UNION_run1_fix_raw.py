@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if start > end:
        raise AssertionError(f"Start value must not be greater than end: start={start}, end={end}")
    # Ensure there's a positive range when count > 0
    if count > 0 and end - start <= 0:
        raise AssertionError(f"Range must be positive: start={start}, end={end}")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )