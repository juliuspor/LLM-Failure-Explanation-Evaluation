@staticmethod
def random(count: int, start: int | None = None, end: int | None = None, letters: bool = False, numbers: bool = False) -> str:
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")

    if start is None and end is None:
        if letters or numbers:
            start = ord(" ")
            end = ord("z") + 1
        else:
            start = 0
            end = 127
    else:
        if start is None:
            start = 0
        if end is None:
            end = 127

    if end <= start:
        raise ValueError(f"end ({end}) must be greater than start ({start})")

    gap = end - start

    buffer: list[str] = []
    while len(buffer) < count:
        ch = chr(start + _RANDOM.randrange(gap))
        if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
            buffer.append(ch)

    return "".join(buffer)