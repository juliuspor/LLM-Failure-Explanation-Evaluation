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

        gap = end - start

        if gap < 0:
            raise ValueError(f"'end' ({end}) must be >= 'start' ({start})")

        buffer: list[str] = []
        if gap == 0:
            ch = chr(start)
            if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
                while len(buffer) < count:
                    buffer.append(ch)
                return "".join(buffer)
            raise ValueError(f"Given range start={start}, end={end} has no valid characters for the requested constraints")

        while len(buffer) < count:
            ch = chr(start + _RANDOM.randrange(gap))
            if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
                buffer.append(ch)

        return "".join(buffer)
