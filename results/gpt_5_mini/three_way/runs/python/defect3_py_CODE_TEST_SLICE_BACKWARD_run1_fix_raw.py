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
        # Sum UTF-16 code units for the consumed codepoints starting at pos
        units = 0
        temp_pos = pos
        for _ in range(consumed):
            if temp_pos >= length:
                break
            cp = code_point_at(code_units, temp_pos)
            units += char_count(cp)
            temp_pos += char_count(cp)
        pos += units
        # safety: avoid infinite loop
        if units == 0:
            pos += 1