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

        # Ensure consumed is positive
        if consumed < 0:
            raise ValueError("Translated consume count must not be negative")

        # Advance pos by the number of UTF-16 code units that represent the consumed codepoints
        advance = 0
        advance_pos = pos
        for _ in range(consumed):
            if advance_pos >= length:
                break
            cp = code_point_at(code_units, advance_pos)
            units = char_count(cp)
            advance += units
            advance_pos += units
        if advance == 0:
            # Prevent infinite loop: if translator claimed to consume but no units advanced, break
            raise ValueError("Translator indicated consumption but no code units were advanced")
        pos += advance
        # continue loop
