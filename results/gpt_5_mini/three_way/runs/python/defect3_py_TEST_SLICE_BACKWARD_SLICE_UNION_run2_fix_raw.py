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

        # Advance pos by the number of UTF-16 code units that represent the consumed codepoints
        units_advanced = 0
        idx = pos
        for _ in range(consumed):
            if idx >= length:
                break
            cu = code_units[idx]
            # If high surrogate and next is low surrogate, consume two units
            if 0xD800 <= cu <= 0xDBFF and idx + 1 < length and 0xDC00 <= code_units[idx + 1] <= 0xDFFF:
                idx += 2
                units_advanced += 2
            else:
                idx += 1
                units_advanced += 1
        pos += units_advanced
