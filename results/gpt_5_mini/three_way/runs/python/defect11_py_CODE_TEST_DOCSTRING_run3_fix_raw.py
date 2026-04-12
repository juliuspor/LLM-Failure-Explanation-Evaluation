@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")
    # If start and end are equal, the range is empty which is invalid unless
    # letters or numbers constraints will select from defaults. To match
    # expected error messaging, raise mentioning start and end.
    if start == end:
        raise ValueError(f"Empty range: start ({start}) and end ({end}) must not be equal")

    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )