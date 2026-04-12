    @staticmethod
    def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
        """
        Creates a random string based on a variety of options.

        The character range is defined by the half-open interval [start, end).
        If `start` and `end` are both zero, a default range is used.
        If `start` and `end` are provided, they must define a valid range (start < end).
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