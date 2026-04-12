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

    if start > end:
        start, end = end, start

    buffer: list[str] = []
    if start == end:
        ch = chr(start)
        while len(buffer) < count:
            if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
                buffer.append(ch)
            else:
                raise ValueError(f"No valid characters in the specified range: start={start}, end={end}, letters={letters}, numbers={numbers}")
        return "".join(buffer)

    gap = end - start
    if gap <= 0:
        raise ValueError(f"end must be greater than start: start={start}, end={end}")

    while len(buffer) < count:
        ch = chr(start + _RANDOM.randrange(gap))
        if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
            buffer.append(ch)

    return "".join(buffer)