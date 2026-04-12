def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return

    code_units = to_utf16_code_units(input_seq)

    pos = 0
    length = len(code_units)

    while pos < length:
        # Attempt translation
        consumed = self.translate_codepoint(code_units, pos, out)
        if consumed == 0:
            # No translator handled this codepoint; copy it to out
            # Safely get the codepoint at current position
            codepoint = code_point_at(code_units, pos)
            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue

        # A translator consumed 'consumed' codepoints. Advance pos by the
        # corresponding number of UTF-16 code units. We must avoid reading
        # beyond the end of code_units while computing char counts.
        for _ in range(consumed):
            if pos >= length:
                break
            cp = code_point_at(code_units, pos)
            pos += char_count(cp)
