@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")
    # Validate start/end
    if start > end:
        raise ValueError(f"Start ({start}) must not be greater than end ({end}).")
    if start == end:
        raise ValueError(f"The range must be non-empty: start ({start}) == end ({end}).")
    # Ensure positive gap to avoid passing non-positive bound to random helper
    gap = end - start
    if gap <= 0:
        raise ValueError(f"Range must be positive: end ({end}) - start ({start}) = {gap} <= 0")
    # Delegate to internal implementation with validation done
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )