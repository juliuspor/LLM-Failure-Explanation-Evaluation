def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return

    # Convert to UTF-16 code units (simulating Java's char[])
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
        # the consumed codepoints. We must not call code_point_at beyond the
        # bounds, so loop carefully and stop if pos reaches length.
        to_advance = 0
        temp_pos = pos
        for _ in range(consumed):
            if temp_pos >= length:
                break
            cp = code_point_at(code_units, temp_pos)
            adv = char_count(cp)
            to_advance += adv
            temp_pos += adv
        pos += to_advance
