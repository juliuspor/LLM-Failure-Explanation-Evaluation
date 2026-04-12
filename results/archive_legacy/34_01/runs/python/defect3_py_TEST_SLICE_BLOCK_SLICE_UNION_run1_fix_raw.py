def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return
    code_units = []
    cp_to_cu = []
    for ch in input_seq:
        cp_to_cu.append(len(code_units))
        cp = ord(ch)
        if cp > 0xFFFF:
            cp -= 0x10000
            high = 0xD800 + (cp >> 10)
            low = 0xDC00 + (cp & 0x3FF)
            code_units.append(high)
            code_units.append(low)
        else:
            code_units.append(cp)
    pos_cp = 0
    length_cp = len(input_seq)
    while pos_cp < length_cp:
        cu_index = cp_to_cu[pos_cp]
        consumed = self.translate_codepoint(code_units, cu_index, out)
        if consumed == 0:
            codepoint = ord(input_seq[pos_cp])
            chars = to_chars(codepoint)
            out.extend(chars)
            pos_cp += 1
            continue
        pos_cp += consumed
