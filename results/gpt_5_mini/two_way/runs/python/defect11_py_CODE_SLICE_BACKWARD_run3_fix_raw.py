@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")

    # If chars range is empty or invalid, adjust to ensure a positive bound.
    # Preserve behavior when callers pass 0/0 to indicate defaults (handled in _random_internal),
    # but if explicit start/end are provided and end <= start, make end = start + 1 to avoid zero/negative bound.
    if not (start == 0 and end == 0) and end <= start:
        end = start + 1

    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )