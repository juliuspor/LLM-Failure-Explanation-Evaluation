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
        pos_increment = 0
        temp_pos = pos
        for _ in range(consumed):
            cp = code_point_at(code_units, temp_pos)
            cnt = char_count(cp)
            temp_pos += cnt
            pos_increment += cnt
        pos += pos_increment
        
    return None