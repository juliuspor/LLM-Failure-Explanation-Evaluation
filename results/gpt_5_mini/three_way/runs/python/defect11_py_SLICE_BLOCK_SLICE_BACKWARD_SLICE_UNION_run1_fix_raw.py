@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")
    # Validate range
    if start >= end:
        raise ValueError(f"Invalid range: start ({start}) must be less than end ({end}).")
    # Ensure bounds are integers
    try:
        start_i = int(start)
        end_i = int(end)
    except Exception:
        raise TypeError("start and end must be integers")
    # Delegate to internal implementation
    return RandomStringUtils._random_internal(
        count=count,
        start=start_i,
        end=end_i,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )