@staticmethod
def random_default(count: int) -> str:
    """
    Creates a random string whose length is the number of characters specified.

    Java equivalent: `RandomStringUtils.random(int count)`.
    """
    return RandomStringUtils._random_internal(count, 0, 0, False, False, None, _RANDOM)