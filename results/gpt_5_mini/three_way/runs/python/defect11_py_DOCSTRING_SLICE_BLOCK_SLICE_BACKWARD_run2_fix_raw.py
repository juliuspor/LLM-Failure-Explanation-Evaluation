@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if end <= start:
        raise ValueError(f"end ({end}) must be greater than start ({start})")
    # If letters/numbers filtering would exclude all characters in the provided range, detect that early.
    # Only perform check when the range is small enough to be reasonable; but for correctness check whole range.
    # Build a quick check: ensure at least one codepoint in [start, end) satisfies filters.
    if letters or numbers:
        found = False
        for cp in range(start, end):
            ch = chr(cp)
            if (letters and ch.isalpha()) or (numbers and ch.isdigit()):
                found = True
                break
        if not found:
            raise ValueError("No characters in the specified range match the letters/numbers constraints")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )