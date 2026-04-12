def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return

    code_units = to_utf16_code_units(input_seq)

    pos = 0
    length = len(code_units)

    while pos < length:
        # Ensure we don't call translate_codepoint with an out-of-range index
        if pos >= length:
            break

        consumed = self.translate_codepoint(code_units, pos, out)
        if consumed == 0:
            # Get the codepoint at current position
            codepoint = code_point_at(code_units, pos)
            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue

        # If a translator reports consuming N codepoints, advance by
        # the corresponding number of UTF-16 code units.
        if consumed < 0:
            # Defensive: treat negative as zero to avoid infinite loop
            consumed = 0

        for _ in range(consumed):
            if pos >= length:
                break
            cp = code_point_at(code_units, pos)
            pos += char_count(cp)
