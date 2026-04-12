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
        # to the 'consumed' code points, without calling code_point_at on
        # invalid indices. Iterate consumed times and count units.
        units = 0
        curr = pos
        for _ in range(consumed):
            if curr >= length:
                break
            cu = code_units[curr]
            if 0xD800 <= cu <= 0xDBFF and curr + 1 < length:
                low = code_units[curr + 1]
                if 0xDC00 <= low <= 0xDFFF:
                    units += 2
                    curr += 2
                    continue
            units += 1
            curr += 1
        pos += units
