def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return

    code_units = to_utf16_code_units(input_seq)

    pos = 0
    length = len(code_units)

    while pos < length:
        # Call translate_codepoint but ensure translator implementations
        # can't cause out-of-range access within this method.
        consumed = self.translate_codepoint(code_units, pos, out)

        if consumed == 0:
            # Safely get the codepoint at current position
            # If pos is somehow out of range, break to avoid IndexError
            try:
                codepoint = code_point_at(code_units, pos)
            except IndexError:
                break
            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue

        # If translator reported consuming more codepoints than remain,
        # clamp to remaining code units to avoid infinite loops or IndexError.
        # We advance pos by the UTF-16 code unit length of each consumed codepoint.
        for _ in range(consumed):
            if pos >= length:
                break
            try:
                cp = code_point_at(code_units, pos)
            except IndexError:
                # Defensive: stop advancing if we can't read more
                pos = length
                break
            pos += char_count(cp)