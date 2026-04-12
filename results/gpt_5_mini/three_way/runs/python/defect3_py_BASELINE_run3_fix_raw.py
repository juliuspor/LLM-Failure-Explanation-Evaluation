def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return

    # Convert to UTF-16 code units (simulating Java's char[])
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

        # Advance pos by the number of UTF-16 code units corresponding to
        # the consumed code points. Do not call code_point_at here to avoid
        # reading index+1 when it may be out of range; instead check for
        # surrogate pairs safely using bounds checks.
        for _ in range(consumed):
            if pos < length and 0xD800 <= code_units[pos] <= 0xDBFF and pos + 1 < length and 0xDC00 <= code_units[pos + 1] <= 0xDFFF:
                pos += 2
            else:
                pos += 1
