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
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError(f"start and end must be integers: start={start!r} end={end!r}")
    if end <= start:
        raise ValueError(f"end must be greater than start: start={start} end={end}")
    gap = end - start
    max_code = start + gap - 1
    if start < 0 or max_code >= 0x110000:
        raise ValueError(f"Requested code point range out of Unicode bounds: start={start} end={end}")
    buffer: list[str] = []
    while len(buffer) < count:
        ch = chr(start + _RANDOM.randrange(gap))
        if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
            buffer.append(ch)
    return "".join(buffer)