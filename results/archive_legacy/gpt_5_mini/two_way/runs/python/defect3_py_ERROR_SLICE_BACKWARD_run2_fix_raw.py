def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return
    code_units = []
    char_to_cu_start = []
    for ch in input_seq:
        char_to_cu_start.append(len(code_units))
        cp = ord(ch)
        if cp > 0xFFFF:
            v = cp - 0x10000
            code_units.append(0xD800 + (v >> 10))
            code_units.append(0xDC00 + (v & 0x3FF))
        else:
            code_units.append(cp)
    pos = 0
    length = len(input_seq)
    while pos < length:
        cu_index = char_to_cu_start[pos]
        consumed = self.translate_codepoint(code_units, cu_index, out)
        if consumed == 0:
            codepoint = code_point_at(code_units, cu_index)
            c = to_chars(codepoint)
            out.extend(c)
            pos += 1
            continue
        pos += consumed