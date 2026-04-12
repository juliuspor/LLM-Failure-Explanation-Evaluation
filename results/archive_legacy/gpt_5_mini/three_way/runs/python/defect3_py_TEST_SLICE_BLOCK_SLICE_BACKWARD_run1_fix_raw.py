def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return
    code_units = to_utf16_code_units(input_seq)
    index_to_codeunit = []
    cu_pos = 0
    for ch in input_seq:
        index_to_codeunit.append(cu_pos)
        cp = ord(ch)
        if cp > 0xFFFF:
            cu_pos += 2
        else:
            cu_pos += 1
    pos_chars = 0
    length_chars = len(index_to_codeunit)
    while pos_chars < length_chars:
        cu_index = index_to_codeunit[pos_chars]
        consumed = self.translate_codepoint(code_units, cu_index, out)
        if consumed == 0:
            codepoint = code_point_at(code_units, cu_index)
            c = to_chars(codepoint)
            out.extend(c)
            pos_chars += 1
            continue
        for _ in range(consumed):
            if pos_chars >= length_chars:
                break
            next_cu = index_to_codeunit[pos_chars]
            cp = code_point_at(code_units, next_cu)
            pos_chars += 1
    return None