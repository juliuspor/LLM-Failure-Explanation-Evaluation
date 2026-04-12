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

        # Determine how many UTF-16 code units correspond to the codepoint
        # at the starting position, then advance by that many units for each
        # consumed codepoint. This avoids calling code_point_at with an
        # out-of-range index inside the loop.
        start_codepoint = code_point_at(code_units, pos)
        unit_count = char_count(start_codepoint)

        # Advance pos by unit_count for each codepoint consumed, but do not
        # exceed the length of the code_units array.
        for _ in range(consumed):
            if pos >= length:
                break
            pos += unit_count
