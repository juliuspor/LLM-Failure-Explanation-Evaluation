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

        # Advance pos by the number of codepoints consumed, converting each
        # consumed codepoint to its UTF-16 code unit length. Guard against
        # running past the end of the array.
        for _ in range(consumed):
            if pos >= length:
                break
            try:
                cp = code_point_at(code_units, pos)
                pos += char_count(cp)
            except IndexError:
                # If somehow out of bounds, advance by one to avoid infinite loop
                pos += 1
