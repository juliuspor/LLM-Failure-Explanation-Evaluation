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

        # Advance pos by the number of UTF-16 code units corresponding to
        # the 'consumed' Unicode code points. Ensure we do not read past
        # the end of the code_units list when determining char counts.
        to_advance = 0
        temp_pos = pos
        for _ in range(consumed):
            if temp_pos >= length:
                # Nothing more to advance; break to avoid IndexError
                break
            cp = code_point_at(code_units, temp_pos)
            units = char_count(cp)
            to_advance += units
            temp_pos += units

        pos += to_advance
