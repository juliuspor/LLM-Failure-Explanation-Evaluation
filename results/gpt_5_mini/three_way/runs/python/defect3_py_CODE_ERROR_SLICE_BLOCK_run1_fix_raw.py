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

        # Ensure consumed does not exceed remaining code units as codepoints
        # Determine remaining codepoints by iterating safely
        remaining = 0
        tmp_pos = pos
        while tmp_pos < length:
            remaining += 1
            cp = code_point_at(code_units, tmp_pos)
            tmp_pos += char_count(cp)
        if consumed > remaining:
            consumed = remaining

        for _ in range(consumed):
            if pos >= length:
                break
            cp = code_point_at(code_units, pos)
            pos += char_count(cp)
