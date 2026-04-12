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
        raise ValueError(f"start ({start}) must be less than end ({end}).")
    candidates: list[str] = []
    for cp in range(start, end):
        ch = chr(cp)
        if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
            candidates.append(ch)
    if not candidates:
        raise ValueError("no characters of requested type in given start/end range")
    buffer: list[str] = []
    for _ in range(count):
        buffer.append(_RANDOM.choice(candidates))
    return "".join(buffer)