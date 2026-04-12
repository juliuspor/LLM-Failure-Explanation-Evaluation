@staticmethod
def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")

    if start == 0 and end == 0:
        if letters or numbers:
            end = ord("z")
            start = ord(" ")
        else:
            end = 126
            start = 0

    if end < start:
        raise ValueError("end must be >= start")

    buffer: list[str] = []
    while len(buffer) < count:
        ch = chr(_RANDOM.randrange(start, end + 1))
        if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
            buffer.append(ch)

    return "".join(buffer)