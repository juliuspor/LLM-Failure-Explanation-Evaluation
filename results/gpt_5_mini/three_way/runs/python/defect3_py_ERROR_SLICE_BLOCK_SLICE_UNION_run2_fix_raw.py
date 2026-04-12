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
            # Get the codepoint at current position, but ensure bounds
            if pos >= length:
                break
            codepoint = code_point_at(code_units, pos)
            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue

        # Ensure consumed is positive and does not drive pos past length
        if consumed < 0:
            # Treat negative as no consumption
            consumed = 0

        # Advance pos by the number of UTF-16 code units that those consumed codepoints occupy.
        advanced = 0
        for _ in range(consumed):
            if pos >= length:
                break
            cp = code_point_at(code_units, pos)
            advanced += char_count(cp)
            pos += char_count(cp)

        # Sanity: do not let pos exceed length
        if pos > length:
            pos = length

        # If translator claimed to consume but didn't advance (malformed), avoid infinite loop
        if advanced == 0 and consumed > 0:
            # Skip one code unit to make progress
            pos += 1
            if pos > length:
                pos = length
