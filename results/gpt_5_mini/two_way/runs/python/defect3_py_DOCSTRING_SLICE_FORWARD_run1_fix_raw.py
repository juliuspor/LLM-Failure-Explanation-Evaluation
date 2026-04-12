def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return

    # Convert to UTF-16 code units (simulating Java's char[])
    code_units = to_utf16_code_units(input_seq)

    # Validate that code_units are integers in 0..0xFFFF
    for i, cu in enumerate(code_units):
        if not isinstance(cu, int):
            raise TypeError(f"code_units element at index {i} is not int: {type(cu).__name__}")
        if cu < 0 or cu > 0xFFFF:
            raise ValueError(f"code unit out of range at index {i}: {cu}")

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

        # Advance pos by the number of UTF-16 code units for each consumed codepoint
        for _ in range(consumed):
            # safety: ensure pos is still valid
            if pos >= length:
                break
            cp = code_point_at(code_units, pos)
            pos += char_count(cp)