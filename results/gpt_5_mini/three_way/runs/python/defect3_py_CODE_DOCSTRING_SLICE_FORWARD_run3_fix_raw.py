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

        # Translator consumed one or more codepoints. Advance pos accordingly.
        # Compute the codepoint at the start once, determine how many UTF-16
        # code units it occupied, and advance by that amount multiplied by
        # the number of consumed codepoints.
        # Ensure we don't loop infinitely: at minimum advance by 1.
        start_codepoint = code_point_at(code_units, pos)
        advance = char_count(start_codepoint)
        if advance < 1:
            advance = 1
        pos += advance * consumed
        # Prevent pos from exceeding length
        if pos > length:
            pos = length
        continue