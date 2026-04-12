def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return
    code_units: List[int] = []
    offsets: List[int] = []
    for ch in input_seq:
        offsets.append(len(code_units))
        cp = ord(ch)
        if cp > 0xFFFF:
            cp -= 0x10000
            high = 0xD800 + (cp >> 10)
            low = 0xDC00 + (cp & 0x3FF)
            code_units.append(high)
            code_units.append(low)
        else:
            code_units.append(cp)
    char_pos = 0
    total_chars = len(offsets)
    while char_pos < total_chars:
        cu_index = offsets[char_pos]
        consumed = self.translate_codepoint(code_units, cu_index, out)
        if consumed == 0:
            codepoint = code_point_at(code_units, cu_index)
            c = to_chars(codepoint)
            out.extend(c)
            char_pos += 1
            continue
        char_pos += consumed