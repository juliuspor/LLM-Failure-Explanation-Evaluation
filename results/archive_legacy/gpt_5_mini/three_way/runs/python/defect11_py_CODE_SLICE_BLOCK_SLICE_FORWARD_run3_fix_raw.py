@staticmethod
def random(count: int, start: int | None = None, end: int | None = None, letters: bool = False, numbers: bool = False) -> str:
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")
    if start is None and end is None:
        if letters or numbers:
            end = ord("z") + 1
            start = ord(" ")
        else:
            end = 127
            start = 0
    elif start is None or end is None:
        raise ValueError("Both start and end must be specified or both must be None")
    gap = end - start
    if gap <= 0:
        raise ValueError(f"end ({end}) must be greater than start ({start})")
    has_valid = False
    for c in range(start, end):
        ch = chr(c)
        if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
            has_valid = True
            break
    if not has_valid:
        raise ValueError("No characters in the specified range match the letters/numbers filters")
    buffer: list[str] = []
    while len(buffer) < count:
        ch = chr(start + _RANDOM.randrange(gap))
        if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
            buffer.append(ch)
    return "".join(buffer)