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

        # consumed is the number of codepoints consumed; advance pos by the
        # corresponding number of UTF-16 code units. Calculate without
        # mutating pos until total is known to avoid index errors.
        units = 0
        temp_index = pos
        for _ in range(consumed):
            if temp_index >= length:
                break
            cp = code_point_at(code_units, temp_index)
            units += char_count(cp)
            temp_index += char_count(cp)
        pos += units
        # continue loop
