@staticmethod
def random_letters_numbers(count: int, letters: bool, numbers: bool) -> str:
    """
    Creates a random string whose length is the number of characters specified.

    Characters will be chosen from the set of alpha-numeric characters as
    indicated by the arguments.

    Java equivalent: `RandomStringUtils.random(int count, boolean letters, boolean numbers)`.
    """
    if letters and numbers:
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    elif letters:
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    elif numbers:
        chars = '0123456789'
    else:
        chars = ''
    return RandomStringUtils._random_internal(count, 0, len(chars), False, False, list(chars), _RANDOM)