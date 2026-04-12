@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    import sys

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

    if start < 0 or end < 0:
        raise ValueError(f"start ({start}) and end ({end}) must be >= 0")
    if end > sys.maxunicode + 1:
        raise ValueError(f"end ({end}) is out of range (must be <= {sys.maxunicode + 1})")
    if end <= start:
        raise ValueError(f"end ({end}) must be greater than start ({start})")

    gap = end - start

    buffer: list[str] = []
    while len(buffer) < count:
        ch = chr(start + _RANDOM.randrange(gap))
        if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
            buffer.append(ch)

    return "".join(buffer)
