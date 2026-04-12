@staticmethod
def random_default(count: int) -> str:
    """
    Creates a random string whose length is the number of characters specified.

    Java equivalent: `RandomStringUtils.random(int count)`.
    """
    return RandomStringUtils._random_internal(count, 0, 0, False, False, None, _RANDOM)

@staticmethod
def random_letters_numbers(count: int, letters: bool, numbers: bool) -> str:
    """
    Creates a random string whose length is the number of characters specified.

    Characters will be chosen from the set of alpha-numeric characters as
    indicated by the arguments.

    Java equivalent: `RandomStringUtils.random(int count, boolean letters, boolean numbers)`.
    """
    return RandomStringUtils._random_internal(count, 0, 0, letters, numbers, None, _RANDOM)