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
            if 0xD800 <= codepoint <= 0xDBFF:
                out.append(0xFFFD)
                pos += 1
                continue
            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue
        for pt in range(consumed):
            current_cp = code_point_at(code_units, pos)
            pos += char_count(current_cp)