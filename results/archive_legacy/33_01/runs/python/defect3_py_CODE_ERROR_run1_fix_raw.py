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
        advance = 0
        p = pos
        for _ in range(consumed):
            if p >= length:
                raise ValueError("translate_codepoint consumed more codepoints than remain")
            cp = code_point_at(code_units, p)
            units = char_count(cp)
            advance += units
            p += units
        pos += advance