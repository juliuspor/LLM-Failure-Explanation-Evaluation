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

        # Advance pos by the number of code points consumed, taking care
        # to account for surrogate pairs (which occupy two code units).
        for _ in range(consumed):
            if pos >= length:
                # Nothing left to advance; break to avoid IndexError
                break
            cu = code_units[pos]
            # If this is a high surrogate and the low surrogate exists, advance by 2
            if 0xD800 <= cu <= 0xDBFF and pos + 1 < length:
                low = code_units[pos + 1]
                if 0xDC00 <= low <= 0xDFFF:
                    pos += 2
                    continue
            # Otherwise advance by 1
            pos += 1
