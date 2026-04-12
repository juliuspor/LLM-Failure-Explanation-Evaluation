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

        # consumed is the number of codepoints consumed starting at pos
        if consumed < 0:
            raise ValueError("translate_codepoint returned negative value")

        # Determine how many UTF-16 code units the consumed codepoints occupy
        start_cp = code_point_at(code_units, pos)
        units_per_cp = char_count(start_cp)
        # If more than one codepoint consumed, we need to sum char_count for each
        # Advance by iterating over the consumed codepoints safely without calling
        # code_point_at beyond bounds.
        consumed_units = 0
        temp_pos = pos
        for _ in range(consumed):
            if temp_pos >= length:
                break
            cp = code_point_at(code_units, temp_pos)
            units = char_count(cp)
            consumed_units += units
            temp_pos += units

        pos += consumed_units
