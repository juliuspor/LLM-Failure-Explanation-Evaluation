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
            chars = to_chars(codepoint)
            out.extend(chars)
            # Advance by number of UTF-16 code units for this codepoint
            pos += len(chars)
            continue

        # Advance pos by the UTF-16 code units corresponding to the consumed codepoints
        advanced = 0
        for _ in range(consumed):
            cp = code_point_at(code_units, pos + advanced)
            advanced += char_count(cp)
        pos += advanced
        continue