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
            cu = code_units[pos]
            if 0xD800 <= cu <= 0xDBFF:
                if pos + 1 < length and 0xDC00 <= code_units[pos + 1] <= 0xDFFF:
                    codepoint = 0x10000 + ((cu - 0xD800) << 10) + (code_units[pos + 1] - 0xDC00)
                    out.extend(to_chars(codepoint))
                    pos += 2
                    continue
                else:
                    out.append(0xFFFD)
                    pos += 1
                    continue
            if 0xDC00 <= cu <= 0xDFFF:
                out.append(0xFFFD)
                pos += 1
                continue
            out.append(cu)
            pos += 1
            continue
        for _ in range(consumed):
            cp = code_point_at(code_units, pos)
            pos += char_count(cp)