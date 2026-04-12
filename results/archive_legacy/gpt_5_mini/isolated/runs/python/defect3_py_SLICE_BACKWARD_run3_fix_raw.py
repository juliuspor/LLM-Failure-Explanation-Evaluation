def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return
    code_units = to_utf16_code_units(input_seq)
    pos = 0
    length = len(code_units)
    while pos < length:
        idx = pos
        if idx < 0:
            idx += length
        if idx < 0 or idx >= length:
            raise IndexError(f"String index out of range: {idx}")
        consumed = self.translate_codepoint(code_units, idx, out)
        if consumed == 0:
            codepoint = code_point_at(code_units, idx)
            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue
        for _ in range(consumed):
            cp_idx = pos
            if cp_idx < 0:
                cp_idx += length
            if cp_idx < 0 or cp_idx >= length:
                raise IndexError(f"String index out of range: {cp_idx}")
            pos += char_count(code_point_at(code_units, cp_idx))
    return None