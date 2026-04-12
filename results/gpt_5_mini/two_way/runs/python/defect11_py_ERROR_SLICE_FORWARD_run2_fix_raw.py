@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if start is None:
        start = 0
    if end is None:
        end = 0
    try:
        start_int = int(start)
        end_int = int(end)
    except (TypeError, ValueError):
        raise ValueError("start and end must be integers or convertible to int")
    if start_int < 0:
        # allow 0 as minimum
        start_int = 0
    if end_int < 0:
        raise ValueError("end must be non-negative")
    if end_int != 0 and end_int <= start_int:
        raise ValueError("end must be greater than start")

    return RandomStringUtils._random_internal(
        count=count,
        start=start_int,
        end=end_int,
        letters=bool(letters),
        numbers=bool(numbers),
        chars=None,
        rnd=_RANDOM,
    )