def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return
    out_temp: List[int] = []
    try:
        result = to_utf16_code_units(input_seq, out_temp)
    except TypeError:
        code_units = to_utf16_code_units(input_seq)
    else:
        if result is None:
            code_units = out_temp
        else:
            code_units = result
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