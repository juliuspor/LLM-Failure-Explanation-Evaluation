def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return
    code_units: List[int] = []
    for ch in input_seq:
        cp = ord(ch)
        if cp > 0xFFFF:
            cp -= 0x10000
            code_units.append(0xD800 + (cp >> 10))
            code_units.append(0xDC00 + (cp & 0x3FF))
        else:
            code_units.append(cp)
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
        for pt in range(consumed):
            pos += char_count(code_point_at(code_units, pos))
