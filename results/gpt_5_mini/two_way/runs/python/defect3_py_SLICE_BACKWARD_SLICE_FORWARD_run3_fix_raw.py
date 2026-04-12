def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return

    # Convert to UTF-16 code units (simulating Java's char[])
    utf16_units = to_utf16_code_units(input_seq)

    pos = 0
    length = len(utf16_units)

    while pos < length:
        consumed = self.translate_codepoint(utf16_units, pos, out)
        if consumed == 0:
            # Get the codepoint at current position
            codepoint = code_point_at(utf16_units, pos)
            chars = to_chars(codepoint)
            out.extend(chars)
            pos += len(chars)
            continue

        # If a translator consumed n codepoints, advance pos by the
        # number of UTF-16 code units those codepoints occupy.
        # We must compute that by examining each consumed codepoint
        # starting at the original pos.
        advance = 0
        cur = pos
        for _ in range(consumed):
            cp = code_point_at(utf16_units, cur)
            advance += char_count(cp)
            cur += char_count(cp)
        pos += advance
