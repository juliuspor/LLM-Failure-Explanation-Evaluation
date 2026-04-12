def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if input_seq is None:
        return
    if out is None:
        raise ValueError("The Writer must not be null")

    code_units = to_utf16_code_units(input_seq)

    pos = 0
    length = len(code_units)

    while pos < length:
        consumed = self.translate_codepoint(code_units, pos, out)
        if consumed == 0:
            codepoint = code_point_at(code_units, pos)
            chars = to_chars(codepoint)
            out.extend(chars)
            pos += len(chars)
            continue

        # Advance pos by the number of UTF-16 code units that correspond to the
        # consumed code points. We iterate consumed times, each time determining
        # the code point at the current position and advancing by its UTF-16
        # code unit length.
        for _ in range(consumed):
            if pos >= length:
                break
            cp = code_point_at(code_units, pos)
            pos += char_count(cp)
