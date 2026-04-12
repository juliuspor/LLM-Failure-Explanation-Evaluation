@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    """
    Creates a random string based on a variety of options.

    The character range is defined by the half-open interval `[start, end)`.
    If `letters` is True, generated characters are restricted to alphabetic
    characters; if `numbers` is True, they are restricted to digits.

    Args:
        count: Length of the generated string.
        start: Lower bound (inclusive) of the character range.
        end: Upper bound (exclusive) of the character range.
        letters: Whether to restrict output to letters.
        numbers: Whether to restrict output to numbers.

    Returns:
        A randomly generated string of length `count`.
    """
    # Ensure meaningful bounds are passed to preserve validation behavior
    effective_start = start if start >= 0 else 0
    effective_end = end if end > effective_start else 128
    return RandomStringUtils._random_internal(
        count=count,
        start=effective_start,
        end=effective_end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )