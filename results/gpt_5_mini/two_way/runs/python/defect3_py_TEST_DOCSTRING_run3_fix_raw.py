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

        # Advance pos by the number of UTF-16 code units that the consumed codepoints occupy
        units_advanced = 0
        for _ in range(consumed):
            # For each codepoint consumed, determine how many code units it uses at the current pos
            cp = code_point_at(code_units, pos)
            units_advanced += char_count(cp)
            pos += char_count(cp)
        # pos is already advanced inside loop; nothing more to do
        # ensure we don't double-advance
        continue