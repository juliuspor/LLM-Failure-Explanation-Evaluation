@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")
    # If count is zero, return empty string immediately (no validation of start/end needed)
    if count == 0:
        return ""
    # For positive count, start must be less than end
    if start >= end:
        raise ValueError(f"Parameter 'start' ({start}) must be less than 'end' ({end}).")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )