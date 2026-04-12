    @staticmethod
    def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
        if start > end:
            raise ValueError(f"Start value {start} must not be greater than end value {end}.")
        if start == end:
            raise ValueError(f"Start value {start} must not be equal to end value {end}.")
        return RandomStringUtils._random_internal(
            count=count,
            start=start,
            end=end,
            letters=letters,
            numbers=numbers,
            chars=None,
            rnd=_RANDOM,
        )