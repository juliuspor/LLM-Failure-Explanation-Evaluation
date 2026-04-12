    @staticmethod
    def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
        """
        Creates a random string based on a variety of options.

        The character range is defined by the half-open interval [start, end).
        If `letters` is True, generated characters are restricted to alphabetic
        characters; if `numbers` is True, they are restricted to numeric characters.

        Args:
            count: Length of the string.
            start: Start of the character range (inclusive).
            end: End of the character range (exclusive).
            letters: Restrict to letters.
            numbers: Restrict to numbers.

        Returns:
            Random string.
        """
        if start >= end:
            raise ValueError(f"start ({start}) must be less than end ({end}).")
        return RandomStringUtils._random_internal(
            count=count,
            start=start,
            end=end,
            letters=letters,
            numbers=numbers,
            chars=None,
            rnd=_RANDOM,
        )