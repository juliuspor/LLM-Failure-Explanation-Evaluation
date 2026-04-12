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
        raise ValueError(f"Invalid range: start ({start}) must be less than end ({end}).")

    gap = end - start

    found = False
    if not letters and not numbers:
        found = True
    else:
        for cp in range(start, end):
            ch = chr(cp)
            if (letters and ch.isalpha()) or (numbers and ch.isdigit()):
                found = True
                break
    if not found:
        raise ValueError(f"No characters in range [{start},{end}) match letters={letters} numbers={numbers}.")

    buffer: list[str] = []
    while len(buffer) < count:
        ch = chr(start + _RANDOM.randrange(gap))
        if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
            buffer.append(ch)

    return "".join(buffer)