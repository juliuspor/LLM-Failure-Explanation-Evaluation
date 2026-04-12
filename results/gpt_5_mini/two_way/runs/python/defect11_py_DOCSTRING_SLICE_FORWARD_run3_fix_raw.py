@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")
    # When chars provided via other wrappers, this method expects start/end bounds over code points.
    # For consistency with random_with_chars/random_from_chars, validate bounds when they may refer to a supplied chars list.
    # Here we simply delegate to _random_internal using the global random source.
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )