def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return
    code_units = to_utf16_code_units(input_seq)
    normalized: List[int] = []
    for cu in code_units:
        if cu > 0xFFFF:
            normalized.extend(to_chars(cu))
        else:
            normalized.append(cu)
    pos = 0
    length = len(normalized)
    while pos < length:
        consumed = self.translate_codepoint(normalized, pos, out)
        if consumed == 0:
            codepoint = code_point_at(normalized, pos)
            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue
        for _ in range(consumed):
            pos += char_count(code_point_at(normalized, pos))