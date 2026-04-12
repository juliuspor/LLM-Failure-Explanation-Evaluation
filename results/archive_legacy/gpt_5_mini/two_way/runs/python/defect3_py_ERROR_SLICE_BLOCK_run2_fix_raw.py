def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return
    code_units = to_utf16_code_units(input_seq)
    pos = 0
    length = len(code_units)
    while pos < length:
        consumed = self.translate_codepoint(code_units, pos, out)
        if consumed == 0:
            codepoint = code_point_at(code_units, pos)
            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue
        advanced = 0
        for _ in range(consumed):
            if pos >= length:
                break
            cp = code_point_at(code_units, pos)
            units = char_count(cp)
            pos += units
            advanced += units
        if advanced == 0:
            raise IndexError(f"String index out of range: {pos}")
    return None