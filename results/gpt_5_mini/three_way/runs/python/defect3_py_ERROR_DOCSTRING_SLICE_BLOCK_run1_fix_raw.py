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

        # Advance pos by the number of UTF-16 code units that represent the
        # consumed code points. Compute safely without reading past the end.
        units_to_advance = 0
        for i in range(consumed):
            cur_index = pos + units_to_advance
            if cur_index >= length:
                # Defensive: nothing more to advance
                break
            cp = code_point_at(code_units, cur_index)
            units_to_advance += char_count(cp)
        pos += units_to_advance
