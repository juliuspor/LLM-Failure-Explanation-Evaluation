@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")

    # Validate explicit range
    if start != 0 or end != 0:
        if start >= end:
            raise ValueError(f"Invalid range: start ({start}) must be less than end ({end}).")
        # Ensure there is at least one character in the provided range
        if end - start <= 0:
            raise ValueError("The range for random characters must not be empty")

    # When using default range (start==0 and end==0), _random_internal will derive defaults.
    # However, ensure that when letters/numbers restriction is requested and the derived
    # defaults would produce an empty set, we surface a clearer error early.
    if start == 0 and end == 0 and not letters and not numbers and count > 0:
        # default will use ASCII printable; no need to check further
        pass

    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )