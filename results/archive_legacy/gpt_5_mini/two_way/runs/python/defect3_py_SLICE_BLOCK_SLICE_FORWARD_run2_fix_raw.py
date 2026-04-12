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
            code_unit = code_units[pos]
            if 0xD800 <= code_unit <= 0xDBFF and pos + 1 < length:
                low = code_units[pos + 1]
                if 0xDC00 <= low <= 0xDFFF:
                    out.append(code_unit)
                    out.append(low)
                    pos += 2
                    continue
            out.append(code_unit)
            pos += 1
            continue
        for _ in range(consumed):
            cp = code_point_at(code_units, pos)
            pos += char_count(cp)
