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
            # Get the codepoint at current position
            codepoint = code_point_at(code_units, pos)
            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue

        # Advance pos by the number of UTF-16 code units corresponding to the
        # consumed codepoints. Be careful with surrogate pairs and bounds.
        units_advanced = 0
        temp_pos = pos
        for _ in range(consumed):
            if temp_pos >= length:
                break
            cu = code_units[temp_pos]
            # If this is a high surrogate and the next unit is a low surrogate, count 2
            if 0xD800 <= cu <= 0xDBFF and temp_pos + 1 < length and 0xDC00 <= code_units[temp_pos + 1] <= 0xDFFF:
                temp_pos += 2
                units_advanced += 2
            else:
                temp_pos += 1
                units_advanced += 1
        pos += units_advanced
