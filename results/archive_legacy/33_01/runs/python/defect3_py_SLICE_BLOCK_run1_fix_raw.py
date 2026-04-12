def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return
    code_units = to_utf16_code_units(input_seq)
    pos = 0
    length = len(code_units)
    import operator
    while pos < length:
        try:
            consumed = self.translate_codepoint(code_units, pos, out)
        except TypeError:
            try:
                pos = operator.index(pos)
            except TypeError:
                raise TypeError(f"index must be an integer or implement __index__; got {type(pos).__name__}")
            continue
        if consumed == 0:
            codepoint = code_point_at(code_units, pos)
            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue
        for pt in range(consumed):
            pos += char_count(code_point_at(code_units, pos))