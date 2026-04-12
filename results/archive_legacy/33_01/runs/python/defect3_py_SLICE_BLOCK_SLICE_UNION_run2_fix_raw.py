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
            cp = code_point_at(code_units, pos)
            units = to_chars(cp)
            out.extend(units)
            pos += len(units)
            continue
        advanced = 0
        for _ in range(consumed):
            cp = code_point_at(code_units, pos)
            advance = char_count(cp)
            pos += advance
            advanced += advance
        if advanced == 0:
            pos += 1
    return None