def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return
    data = input_seq.encode('utf-16-le')
    code_units = [data[i] | (data[i+1] << 8) for i in range(0, len(data), 2)]
    pos = 0
    length = len(code_units)
    while pos < length:
        consumed = self.translate_codepoint(code_units, pos, out)
        if consumed == 0:
            high = code_units[pos]
            if 0xD800 <= high <= 0xDBFF and pos + 1 < length:
                low = code_units[pos + 1]
                if 0xDC00 <= low <= 0xDFFF:
                    out.append(high)
                    out.append(low)
                    pos += 2
                    continue
            out.append(high)
            pos += 1
            continue
        for _ in range(consumed):
            cp = code_point_at(code_units, pos)
            c = to_chars(cp)
            out.extend(c)
            pos += len(c)