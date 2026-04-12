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

        # Advance pos by the number of code units that correspond to the
        # consumed codepoints. For each consumed codepoint, determine its
        # UTF-16 code unit length at the current pos and advance accordingly.
        consumed_left = consumed
        while consumed_left > 0 and pos < length:
            cp = code_point_at(code_units, pos)
            pos += char_count(cp)
            consumed_left -= 1
