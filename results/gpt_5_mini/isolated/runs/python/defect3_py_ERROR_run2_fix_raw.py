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
        if consumed < 0:
            raise ValueError("translate_codepoint returned negative value")
        # Advance pos by the number of UTF-16 code units that correspond to the
        # consumed codepoints, taking care not to read past the end.
        units_advanced = 0
        for i in range(consumed):
            if pos + units_advanced >= length:
                # Avoid IndexError: stop advancing if there are no more code units
                break
            cp = code_point_at(code_units, pos + units_advanced)
            units_advanced += char_count(cp)
        # Ensure we make progress to avoid infinite loops
        if units_advanced == 0:
            # As a fallback, move forward by one code unit
            units_advanced = 1
        pos += units_advanced
        # Continue the loop
        continue