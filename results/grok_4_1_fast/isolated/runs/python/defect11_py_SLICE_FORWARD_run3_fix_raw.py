@staticmethod
def random(count: int) -> str:
    """
    Creates a random string whose length is the number of characters specified.

    Java equivalent: `RandomStringUtils.random(int count)`.
    """
    return RandomStringUtils.random_default(count)