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
            # No translator consumed anything: copy the codepoint at pos
            codepoint = code_point_at(code_units, pos)
            chars = to_chars(codepoint)
            out.extend(chars)
            pos += len(chars)
            continue

        # One or more codepoints were consumed by the translator.
        # Advance pos by the total number of UTF-16 code units those codepoints occupied.
        temp_pos = pos
        for _ in range(consumed):
            if temp_pos >= length:
                break
            cp = code_point_at(code_units, temp_pos)
            temp_pos += char_count(cp)
        pos = temp_pos