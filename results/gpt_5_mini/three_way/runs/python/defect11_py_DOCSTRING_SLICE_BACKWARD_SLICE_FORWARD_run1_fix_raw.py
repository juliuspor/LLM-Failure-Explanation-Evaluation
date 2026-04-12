@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("start and end must be integers")
    if end <= start:
        raise ValueError(f"Invalid range: start ({start}) must be less than end ({end}).")
    # If letters or numbers are requested, ensure that the range contains at least one valid char
    if letters or numbers:
        found = False
        for code_point in range(start, end):
            ch = chr(code_point)
            if (letters and ch.isalpha()) or (numbers and ch.isdigit()):
                found = True
                break
        if not found:
            raise ValueError("No characters in the specified range satisfy the letters/numbers constraints")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )