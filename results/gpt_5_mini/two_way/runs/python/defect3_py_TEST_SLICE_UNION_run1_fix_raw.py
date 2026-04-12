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
            # Get the codepoint at current position
            codepoint = code_point_at(code_units, pos)
            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue

        # consumed is a count of codepoints consumed; advance pos by the
        # corresponding number of UTF-16 code units. Iterate consumed times,
        # each time reading the codepoint at the current UTF-16 index and
        # advancing by its UTF-16 length. Also guard against running past the
        # end of the code_units list.
        for _ in range(consumed):
            if pos >= length:
                break
            cp = code_point_at(code_units, pos)
            pos += char_count(cp)
