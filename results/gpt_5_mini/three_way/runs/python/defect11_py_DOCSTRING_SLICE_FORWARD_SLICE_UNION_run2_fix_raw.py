@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if start >= end:
        raise ValueError(
            f"Invalid range: start ({start}) must be less than end ({end})."
        )
    # Quick sanity: ensure there is at least one possible character given letters/numbers
    if letters or numbers:
        # Check if the provided range contains any valid char
        found = False
        for cp in range(start, end):
            ch = chr(cp)
            if (letters and ch.isalpha()) or (numbers and ch.isdigit()):
                found = True
                break
        if not found:
            raise ValueError(
                f"No characters in range [{start}, {end}) match letters={letters} numbers={numbers}."
            )
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )