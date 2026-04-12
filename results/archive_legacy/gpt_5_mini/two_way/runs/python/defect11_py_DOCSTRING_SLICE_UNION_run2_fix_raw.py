@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")

    if start == 0 and end == 0:
        if letters or numbers:
            start = ord(" ")
            end = ord("z")
        else:
            start = 0
            end = 126

    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("start and end must be integers")

    if start < 0 or end < 0:
        raise ValueError("start and end must be non-negative")

    if end < start:
        raise ValueError(f"end ({end}) must be >= start ({start})")

    buffer: list[str] = []
    while len(buffer) < count:
        ch = chr(_RANDOM.randrange(start, end + 1))
        if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
            buffer.append(ch)

    return "".join(buffer)