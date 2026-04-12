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

        # Advance pos by the number of UTF-16 code units corresponding to
        # the 'consumed' codepoints handled by the translator.
        units_advanced = 0
        count = 0
        while count < consumed and pos + units_advanced < length:
            cp = code_point_at(code_units, pos + units_advanced)
            units_advanced += char_count(cp)
            count += 1
        pos += units_advanced
        # If translators claimed to consume more codepoints than available,
        # break to avoid infinite loop.
        if units_advanced == 0:
            break
