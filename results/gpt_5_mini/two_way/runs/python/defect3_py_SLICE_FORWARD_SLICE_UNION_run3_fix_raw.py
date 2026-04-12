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
            # No translation; copy current code unit(s) preserving surrogates
            cu = code_units[pos]
            # If current is high surrogate and next is low surrogate, copy both
            if 0xD800 <= cu <= 0xDBFF and pos + 1 < length:
                low = code_units[pos + 1]
                if 0xDC00 <= low <= 0xDFFF:
                    out.append(cu)
                    out.append(low)
                    pos += 2
                    continue
            # Otherwise copy single code unit
            out.append(cu)
            pos += 1
            continue

        # Advance pos by number of UTF-16 code units consumed for each codepoint
        for _ in range(consumed):
            cp = code_point_at(code_units, pos)
            pos += char_count(cp)