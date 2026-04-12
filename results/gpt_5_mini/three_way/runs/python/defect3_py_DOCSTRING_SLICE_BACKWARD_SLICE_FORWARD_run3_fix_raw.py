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
            pos += len(chars)
        else:
            # Advance by the number of code points consumed.
            # Each code point may be 1 or 2 UTF-16 code units; sum their char counts.
            advance = 0
            for i in range(consumed):
                if pos + advance >= length:
                    break
                cp = code_point_at(code_units, pos + advance)
                advance += char_count(cp)
            pos += advance
