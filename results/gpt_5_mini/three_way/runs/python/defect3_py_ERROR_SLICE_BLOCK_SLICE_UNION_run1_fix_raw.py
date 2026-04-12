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
        # Ensure we don't call translate_codepoint with pos out of range
        consumed = self.translate_codepoint(code_units, pos, out)
        if consumed == 0:
            # Get the codepoint at current position
            codepoint = code_point_at(code_units, pos)
            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue

        # If translator consumed N codepoints, advance pos by the number of UTF-16 code units
        # those codepoints occupy.
        units_advanced = 0
        for _ in range(consumed):
            if pos < length:
                cp = code_point_at(code_units, pos)
                units_advanced += char_count(cp)
                pos += char_count(cp)
            else:
                break
        # pos already updated in loop; continue to next iteration
        continue