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

        # Advance pos by the number of UTF-16 code units that correspond
        # to the 'consumed' codepoints, without reading past the end.
        units_advanced = 0
        cur = pos
        for _ in range(consumed):
            if cur >= length:
                break
            cu = code_units[cur]
            # if high surrogate and next is low surrogate, consume 2 units
            if 0xD800 <= cu <= 0xDBFF and cur + 1 < length and 0xDC00 <= code_units[cur + 1] <= 0xDFFF:
                cur += 2
                units_advanced += 2
            else:
                cur += 1
                units_advanced += 1
        pos += units_advanced
        # Ensure we always make progress
        if units_advanced == 0:
            pos += 1
