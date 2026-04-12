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
            # No translator consumed codepoints: copy the current codepoint (could be surrogate pair)
            codepoint = code_point_at(code_units, pos)
            chars = to_chars(codepoint)
            out.extend(chars)
            pos += len(chars)
            continue

        # If translators consumed N codepoints, advance pos by the UTF-16 unit length of those codepoints
        for _ in range(consumed):
            cp = code_point_at(code_units, pos)
            pos += char_count(cp)
