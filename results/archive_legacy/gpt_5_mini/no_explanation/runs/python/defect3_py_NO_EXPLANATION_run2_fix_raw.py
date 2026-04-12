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

        # consumed is number of codepoints; advance pos by the UTF-16 code units
        # that those codepoints occupied. We iterate consumed times to account
        # for surrogate pairs properly and avoid indexing errors.
        if consumed < 0:
            raise ValueError(f"Invalid consume count: {consumed}")

        advanced = 0
        for _ in range(consumed):
            if pos >= length:
                # Nothing more to advance
                break
            cp = code_point_at(code_units, pos)
            units = char_count(cp)
            pos += units
            advanced += units

        # If translator claimed to consume more codepoints than available, stop.
        if advanced == 0 and consumed > 0:
            break

        # continue loop
        
