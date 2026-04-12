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
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("start and end must be integers")
    gap = end - start + 1
    if gap <= 0:
        raise ValueError(f"bound must be positive: start={start}, end={end}")
    buffer: list[str] = []
    while len(buffer) < count:
        ch = chr(start + _RANDOM.randrange(gap))
        if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
            buffer.append(ch)
    return "".join(buffer)