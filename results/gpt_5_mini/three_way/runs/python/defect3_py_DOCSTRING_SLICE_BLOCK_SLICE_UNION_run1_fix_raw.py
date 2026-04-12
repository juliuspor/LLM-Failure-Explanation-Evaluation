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

        # Ensure consumed is not larger than remaining code points
        # Convert consumed (count of codepoints) into code units advanced
        remaining = length - pos
        # Compute how many codepoints actually remain by iterating safely
        actual_advance_units = 0
        cp_count = 0
        temp_pos = pos
        while cp_count < consumed and temp_pos < length:
            cp = code_point_at(code_units, temp_pos)
            advance = char_count(cp)
            actual_advance_units += advance
            temp_pos += advance
            cp_count += 1

        # Advance pos by the computed code units (safe)
        pos += actual_advance_units
