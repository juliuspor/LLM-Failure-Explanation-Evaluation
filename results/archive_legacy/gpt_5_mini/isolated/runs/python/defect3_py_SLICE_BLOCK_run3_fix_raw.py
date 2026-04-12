def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return
    import numbers
    code_units = to_utf16_code_units(input_seq)
    pos = 0
    length = len(code_units)
    while pos < length:
        consumed = self.translate_codepoint(code_units, pos, out)
        if not isinstance(consumed, numbers.Integral):
            raise TypeError(f"translate_codepoint must return int, got {type(consumed).__name__}")
        if consumed < 0:
            raise ValueError(f"translate_codepoint returned negative value: {consumed}")
        if consumed == 0:
            codepoint = code_point_at(code_units, pos)
            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue
        remaining = length - pos
        max_codepoints = remaining
        if consumed > max_codepoints:
            raise IndexError(f"consume count {consumed} exceeds available codepoints {max_codepoints}")
        for _ in range(int(consumed)):
            cp = code_point_at(code_units, pos)
            pos += char_count(cp)
