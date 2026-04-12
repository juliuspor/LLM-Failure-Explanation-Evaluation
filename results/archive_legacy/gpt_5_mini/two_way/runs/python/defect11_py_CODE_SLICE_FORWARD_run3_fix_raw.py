@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("start and end must be integers")
    if start == 0 and end == 0:
        if letters or numbers:
            end = ord("z") + 1
            start = ord(" ")
        else:
            end = 127
            start = 0
    if end <= start:
        raise ValueError(f"end ({end}) must be greater than start ({start})")
    if start < 0 or end > 0x110000:
        raise ValueError(f"start and end must be within valid Unicode range: 0 <= start < end <= 0x110000, got start={start}, end={end}")
    gap = end - start
    buffer: list[str] = []
    while len(buffer) < count:
        ch = chr(start + _RANDOM.randrange(gap))
        if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
            buffer.append(ch)
    return "".join(buffer)