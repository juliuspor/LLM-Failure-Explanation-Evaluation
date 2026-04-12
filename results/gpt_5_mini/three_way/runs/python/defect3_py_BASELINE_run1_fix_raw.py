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

        # Advance pos by the number of UTF-16 code units that the consumed
        # code points occupy. Avoid calling code_point_at with an out-of-range index.
        consumed_units = 0
        for _ in range(consumed):
            if pos + consumed_units >= length:
                break
            cp = code_point_at(code_units, pos + consumed_units)
            consumed_units += char_count(cp)
        pos += consumed_units
        # If consumed_units is zero (defensive), break to avoid infinite loop
        if consumed_units == 0:
            break
