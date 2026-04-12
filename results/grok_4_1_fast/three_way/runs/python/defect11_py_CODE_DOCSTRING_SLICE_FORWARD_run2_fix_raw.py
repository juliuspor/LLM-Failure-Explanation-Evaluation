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
    if letters or numbers:
        if letters and numbers:
            return RandomStringUtils.random_letters_numbers(count, letters=True, numbers=True)
        elif letters:
            return RandomStringUtils.random_letters_numbers(count, letters=True, numbers=False)
        else:  # numbers
            return RandomStringUtils.random_letters_numbers(count, letters=False, numbers=True)
    else:
        return RandomStringUtils._random_internal(
            count=count,
            start=start,
            end=end,
            letters=False,
            numbers=False,
            chars=None,
            rnd=_RANDOM,
        )