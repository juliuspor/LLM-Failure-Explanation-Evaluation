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

        # Advance pos by the number of UTF-16 code units corresponding
        # to the consumed codepoints without calling code_point_at which
        # could read past the end. For each consumed codepoint, check if
        # the current code unit is a high surrogate and the next is a low
        # surrogate; if so advance by 2, else advance by 1.
        for _ in range(consumed):
            if pos >= length:
                break
            cu = code_units[pos]
            if 0xD800 <= cu <= 0xDBFF and pos + 1 < length:
                low = code_units[pos + 1]
                if 0xDC00 <= low <= 0xDFFF:
                    pos += 2
                    continue
            pos += 1