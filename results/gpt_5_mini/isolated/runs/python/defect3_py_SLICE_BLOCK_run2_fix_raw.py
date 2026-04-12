def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return

    code_units = to_utf16_code_units(input_seq)

    pos = 0
    length = len(code_units)

    while pos < length:
        # Ensure translate_codepoint is called with valid index
        if pos < 0 or pos >= length:
            # Defensive: break to avoid IndexError
            break

        consumed = self.translate_codepoint(code_units, pos, out)
        if consumed == 0:
            # Get the codepoint at current position
            # Safe because pos < length
            codepoint = code_point_at(code_units, pos)
            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue

        # Validate consumed
        if consumed < 0:
            raise ValueError(f"Invalid consumed count: {consumed}")

        # Advance pos by the number of UTF-16 code units consumed
        advanced = 0
        for _ in range(consumed):
            if pos >= length:
                # Defensive: stop advancing if at end
                break
            cp = code_point_at(code_units, pos)
            cu_count = char_count(cp)
            pos += cu_count
            advanced += cu_count

        # If translator claimed to consume codepoints but didn't advance, stop to prevent infinite loop
        if advanced == 0 and pos < length:
            # Fallback: advance by one code unit
            pos += 1
