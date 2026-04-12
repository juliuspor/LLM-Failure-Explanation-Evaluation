def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return
    data = input_seq.encode('utf-16-le')
    code_units = [int.from_bytes(data[i:i+2], 'little') for i in range(0, len(data), 2)]
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
        for pt in range(consumed):
            pos += char_count(code_point_at(code_units, pos))
    return None