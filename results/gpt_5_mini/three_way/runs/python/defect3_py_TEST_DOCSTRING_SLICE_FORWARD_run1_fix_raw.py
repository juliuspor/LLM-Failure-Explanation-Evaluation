def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return

    # Convert to UTF-16 code units (list of 0..0xFFFF ints)
    code_units = to_utf16_code_units(input_seq)

    pos = 0
    length = len(code_units)

    while pos < length:
        consumed = self.translate_codepoint(code_units, pos, out)
        if consumed == 0:
            # Get the codepoint at current position
            codepoint = code_point_at(code_units, pos)
            chars = to_chars(codepoint)
            out.extend(chars)
            # Advance by number of UTF-16 code units for this codepoint
            pos += char_count(codepoint)
            continue

        # If translator consumed n codepoints, advance by the corresponding
        # number of UTF-16 code units for each consumed codepoint.
        for _ in range(consumed):
            cp = code_point_at(code_units, pos)
            pos += char_count(cp)