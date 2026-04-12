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
        raise TypeError("start and end must be integers")

    if not (0 <= start <= 0x10FFFF) or not (0 <= end <= 0x110000):
        raise ValueError(f"start and end must be in valid Unicode range: got start={start}, end={end}")

    if end <= start:
        raise ValueError(f"end ({end}) must be greater than start ({start})")

    buffer: list[str] = []
    while len(buffer) < count:
        val = _RANDOM.randrange(start, end)
        if not (0 <= val <= 0x10FFFF):
            raise ValueError(f"generated code point out of range: {val}")
        ch = chr(val)
        if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
            buffer.append(ch)

    return "".join(buffer)
