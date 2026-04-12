    @staticmethod
    def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
        """
        Creates a random string based on a variety of options.

        The character range is defined by the half-open interval `[start, end)`.
        If `letters` is True, generated characters are restricted to alphabetic
        characters; if `numbers` is True, they are restricted to digits.

        Args:
            count: length of the random string.
            start: start of the character range (inclusive).
            end: end of the character range (exclusive).
            letters: restrict to letters.
            numbers: restrict to digits.

        Returns:
            A randomly generated string.
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