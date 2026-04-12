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
            if 0xD800 <= cu <= 0xDBFF and pos + 1 < length:
                low = code_units[pos + 1]
                if 0xDC00 <= low <= 0xDFFF:
                    codepoint = 0x10000 + ((cu - 0xD800) << 10) + (low - 0xDC00)
                    chars = to_chars(codepoint)
                    out.extend(chars)
                    pos += len(chars)
                    continue
            out.append(cu)
            pos += 1
            continue
        pos += consumed
