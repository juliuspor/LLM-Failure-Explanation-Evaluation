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
            # Get the codepoint at current position (handle surrogate pairs safely)
            cu = code_units[pos]
            if 0xD800 <= cu <= 0xDBFF and pos + 1 < length and 0xDC00 <= code_units[pos + 1] <= 0xDFFF:
                # surrogate pair
                codepoint = 0x10000 + ((cu - 0xD800) << 10) + (code_units[pos + 1] - 0xDC00)
                out.extend([cu, code_units[pos + 1]])
                pos += 2
            else:
                out.append(cu)
                pos += 1
            continue

        # Advance pos by the number of UTF-16 code units corresponding to the consumed codepoints
        for _ in range(consumed):
            if pos >= length:
                break
            cu = code_units[pos]
            if 0xD800 <= cu <= 0xDBFF and pos + 1 < length and 0xDC00 <= code_units[pos + 1] <= 0xDFFF:
                pos += 2
            else:
                pos += 1
