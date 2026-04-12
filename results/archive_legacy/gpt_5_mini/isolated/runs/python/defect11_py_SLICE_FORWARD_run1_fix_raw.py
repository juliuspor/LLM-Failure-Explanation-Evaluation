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
    if end <= start:
        raise ValueError(f"Invalid start ({start}) and end ({end}) range: end must be greater than start")
    gap = end - start
    if start < 0 or start > 0x10FFFF or gap <= 0 or start + gap - 1 > 0x10FFFF:
        raise ValueError(f"Invalid code point range: start={start}, end={end}")
    buffer: list[str] = []
    while len(buffer) < count:
        ch = chr(start + _RANDOM.randrange(gap))
        if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
            buffer.append(ch)
    return "".join(buffer)