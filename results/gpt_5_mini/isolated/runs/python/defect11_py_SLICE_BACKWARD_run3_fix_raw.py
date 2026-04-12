@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )


def _next_int_java(rnd: random.Random, bound: int) -> int:
    """
    Java-like `Random#nextInt(bound)` helper.

    Java throws `IllegalArgumentException("bound must be positive")` when
    `bound <= 0`. This helper preserves that error message.
    """
    # Type validation: ensure numeric bound
    if not isinstance(bound, (int, float)):
        raise TypeError("bound must be an int or float")
    # Now check positivity for numeric types
    if bound <= 0:
        raise ValueError("bound must be positive")
    return rnd.randrange(int(bound))