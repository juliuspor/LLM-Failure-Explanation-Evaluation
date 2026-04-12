@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")
    # Validate range: allow start==end==0 as meaning defaults; otherwise start must be less than end
    if not (start == 0 and end == 0):
        if start > end:
            raise ValueError(f"Invalid range: start={start} end={end}")
        if start == end:
            # If start == end but not both zero, it's an empty range -> error
            raise ValueError(f"Invalid range: start={start} end={end}")
    return RandomStringUtils._random_internal(
        count=count,
        start=start,
        end=end,
        letters=letters,
        numbers=numbers,
        chars=None,
        rnd=_RANDOM,
    )