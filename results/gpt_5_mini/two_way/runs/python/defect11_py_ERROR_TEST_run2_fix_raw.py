@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")
    # Validate the provided range up front so we raise a descriptive error
    if start > end:
        raise ValueError(f"start ({start}) must not be greater than end ({end})")
    if start == end:
        raise ValueError(f"start ({start}) and end ({end}) must not be equal")

    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )