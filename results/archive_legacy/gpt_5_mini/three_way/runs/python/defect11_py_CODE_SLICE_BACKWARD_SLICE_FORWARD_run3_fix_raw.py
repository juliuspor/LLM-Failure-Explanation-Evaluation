@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")

    if start == 0 and end == 0:
        if letters or numbers:
            end = ord("z") + 1
            start = ord(" ")
        else:
            end = 127
            start = 0

    import sys

    if not (isinstance(start, int) and isinstance(end, int)):
        raise ValueError(f"start and end must be integers: start={start}, end={end}")
    if start < 0 or end < 0 or start > sys.maxunicode or end > sys.maxunicode:
        raise ValueError(f"start and end must be valid Unicode code points: start={start}, end={end}")
    if start > end:
        raise ValueError(f"start ({start}) must be <= end ({end})")
    if start == end:
        raise ValueError(f"start ({start}) must be < end ({end})")

    gap = end - start

    if gap <= 0:
        raise ValueError("bound must be positive")

    buffer: list[str] = []
    while len(buffer) < count:
        ch = chr(start + _RANDOM.randrange(gap))
        if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
            buffer.append(ch)

    return "".join(buffer)
