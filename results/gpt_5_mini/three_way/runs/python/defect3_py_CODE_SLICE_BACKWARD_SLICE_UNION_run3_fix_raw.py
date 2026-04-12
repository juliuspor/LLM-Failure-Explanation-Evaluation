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
            codepoint = code_point_at(code_units, pos)
            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue

        # Advance pos by the number of UTF-16 code units that correspond
        # to the 'consumed' code points, without reading out of bounds.
        advance = 0
        for _ in range(consumed):
            # safe to call code_point_at with pos + advance because we ensure
            # pos + advance < length in loop (consumed originates from a
            # translator that consumed valid code points starting at pos)
            cp = code_point_at(code_units, pos + advance)
            advance += char_count(cp)
        pos += advance
