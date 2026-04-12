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

        # Advance pos by the number of UTF-16 code units corresponding to the
        # consumed code points. Do this by inspecting the code_units directly
        # without calling code_point_at which may read beyond bounds.
        for _ in range(consumed):
            if pos >= length:
                # Nothing more to advance; break to avoid IndexError
                break
            cu = code_units[pos]
            # If this is a high surrogate and a following low surrogate exists,
            # count as 2 code units, else count as 1.
            if 0xD800 <= cu <= 0xDBFF and pos + 1 < length and 0xDC00 <= code_units[pos + 1] <= 0xDFFF:
                pos += 2
            else:
                pos += 1
