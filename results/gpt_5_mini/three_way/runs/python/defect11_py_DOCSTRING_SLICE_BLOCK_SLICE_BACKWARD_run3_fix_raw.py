@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")

    # If start and end are both zero, _random_internal would derive defaults. We keep behavior
    # consistent by delegating to _random_internal when start==end==0.
    if start == 0 and end == 0:
        return RandomStringUtils._random_internal(count, start, end, letters, numbers, None, _RANDOM)

    # Validate range
    if end <= start:
        raise ValueError(f"Invalid range: end ({end}) must be greater than start ({start}).")

    # Ensure there is at least one candidate in the provided range that matches letters/numbers
    # If chars isn't provided, the candidate set is code points in [start, end).
    gap = end - start
    if gap <= 0:
        raise ValueError(f"Invalid range: computed bound {gap} is not positive for start={start}, end={end}.")

    # Delegate to internal implementation
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )