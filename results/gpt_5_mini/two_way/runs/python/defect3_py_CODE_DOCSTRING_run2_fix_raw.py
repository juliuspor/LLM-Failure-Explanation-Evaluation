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

        # Advance pos by the number of UTF-16 code units spanned by the
        # consumed codepoints. For each consumed codepoint, read the
        # codepoint at the current pos and advance by its UTF-16 length.
        initial_pos = pos
        for _ in range(consumed):
            if pos >= length:
                # Defensive: consumed more codepoints than available
                raise IndexError("Consumed more codepoints than available in input")
            cp = code_point_at(code_units, pos)
            adv = char_count(cp)
            if adv <= 0:
                raise RuntimeError("Invalid char count while advancing position")
            pos += adv
        if pos <= initial_pos:
            raise RuntimeError("Translator did not advance position; potential infinite loop")
