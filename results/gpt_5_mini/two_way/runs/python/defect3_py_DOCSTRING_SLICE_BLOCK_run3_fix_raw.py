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

        # consumed is number of code points consumed; advance pos by the
        # corresponding number of UTF-16 code units, with bounds checks.
        advanced = 0
        for _ in range(consumed):
            if pos >= length:
                # Defensive: avoid IndexError if translator indicated more
                # code points than remain. Stop advancing.
                break
            cp = code_point_at(code_units, pos)
            units = char_count(cp)
            pos += units
            advanced += units
        # If advanced == 0 and consumed > 0, avoid infinite loop by moving forward one.
        if advanced == 0 and consumed > 0:
            # fallback: consume one code unit to make progress
            pos += 1
