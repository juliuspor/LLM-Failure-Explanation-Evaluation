def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return

    code_units = to_utf16_code_units(input_seq)

    def _code_point_at(code_units: List[int], index: int) -> (int, int):
        if index < 0 or index >= len(code_units):
            raise IndexError(f"String index out of range: {index}")
        high = code_units[index]
        if 0xD800 <= high <= 0xDBFF and index + 1 < len(code_units):
            low = code_units[index + 1]
            if 0xDC00 <= low <= 0xDFFF:
                cp = 0x10000 + ((high - 0xD800) << 10) + (low - 0xDC00)
                return cp, 2
        return high, 1

    pos = 0
    length = len(code_units)

    while pos < length:
        consumed = self.translate_codepoint(code_units, pos, out)
        if consumed == 0:
            codepoint, count = _code_point_at(code_units, pos)
            c = to_chars(codepoint)
            out.extend(c)
            pos += count
            continue

        for _ in range(consumed):
            codepoint, count = _code_point_at(code_units, pos)
            pos += count
