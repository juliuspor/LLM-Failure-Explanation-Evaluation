def translate(self, input_seq: Optional[object], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return
    if isinstance(input_seq, str):
        code_units = to_utf16_code_units(input_seq)
    elif isinstance(input_seq, list) and all(isinstance(x, int) for x in input_seq):
        code_units = input_seq
    else:
        raise TypeError("input_seq must be a str or a list of integers")
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
        for _ in range(consumed):
            cp = code_point_at(code_units, pos)
            pos += char_count(cp)