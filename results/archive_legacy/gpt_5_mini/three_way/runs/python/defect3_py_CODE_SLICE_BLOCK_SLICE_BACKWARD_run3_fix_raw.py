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
        remaining = length - pos
        expected_min_units = consumed
        units_count = 0
        temp_pos = pos
        for _ in range(consumed):
            if temp_pos >= length:
                raise ValueError(f"translate_codepoint consumed {consumed} codepoints starting at {pos}, but only {remaining} code unit(s) remain")
            cu = code_units[temp_pos]
            if 0xD800 <= cu <= 0xDBFF and temp_pos + 1 < length and 0xDC00 <= code_units[temp_pos + 1] <= 0xDFFF:
                temp_pos += 2
                units_count += 2
            else:
                temp_pos += 1
                units_count += 1
        pos += units_count