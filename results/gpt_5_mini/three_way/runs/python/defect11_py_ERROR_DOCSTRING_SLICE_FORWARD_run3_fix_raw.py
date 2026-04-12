@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")

    # Derive defaults consistent with _random_internal behavior
    if start == 0 and end == 0:
        if letters or numbers:
            end = ord('z') + 1
            start = ord(' ')
        else:
            end = 127
            start = 0

    if end <= start:
        raise ValueError(f"Invalid range: start ({start}) must be less than end ({end}).")

    gap = end - start
    if gap <= 0:
        raise ValueError(f"Invalid range: start ({start}) must be less than end ({end}).")

    # If letters or numbers filters are requested, verify that the range contains at least one
    # suitable character. We sample the range to check; for performance use direct scan when gap is small,
    # otherwise check by iterating through the range until a match is found or exhausted.
    if letters or numbers:
        found = False
        # If gap is large, limit check to full scan but that's still bounded by gap size; it's acceptable here.
        for code_point in range(start, end):
            ch = chr(code_point)
            if (letters and ch.isalpha()) or (numbers and ch.isdigit()):
                found = True
                break
        if not found:
            raise ValueError(f"No characters in range [{start}, {end}) match the requested filters (letters={letters}, numbers={numbers}).")

    # Delegate to internal implementation using the validated/derived bounds
    return RandomStringUtils._random_internal(count=count, start=start, end=end, letters=letters, numbers=numbers, chars=None, rnd=_RANDOM)