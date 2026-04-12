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
            high = code_units[pos]
            if 0xD800 <= high <= 0xDBFF and pos + 1 < length and 0xDC00 <= code_units[pos + 1] <= 0xDFFF:
                codepoint = 0x10000 + ((high - 0xD800) << 10) + (code_units[pos + 1] - 0xDC00)
                c = to_chars(codepoint)
                out.extend(c)
                pos += 2
            else:
                out.extend(to_chars(high))
                pos += 1
            continue
        for _ in range(consumed):
            if pos >= length:
                break
            high = code_units[pos]
            if 0xD800 <= high <= 0xDBFF and pos + 1 < length and 0xDC00 <= code_units[pos + 1] <= 0xDFFF:
                pos += 2
            else:
                pos += 1