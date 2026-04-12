    @staticmethod
    def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
        if (letters or numbers) and start <= 0:
            raise ValueError("start must be positive")
        return RandomStringUtils._random_internal(
            count=count,
            start=start,
            end=end,
            letters=letters,
            numbers=numbers,
            chars=None,
            rnd=_RANDOM,
        )