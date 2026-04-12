def _next_int_java(rnd: random.Random, bound: int, start: int = 0) -> int:
    """
    Java-like `Random#nextInt(bound)` helper.

    Java throws `IllegalArgumentException("bound must be positive")` when
    `bound <= 0`. This helper preserves that error message.
    """
    if bound <= 0:
        raise ValueError(f"start {start} + gap {bound} must be positive")
    return rnd.randrange(bound)

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
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )