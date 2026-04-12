def translate(self, input_seq: Optional[str], out: Optional[List[int]] = None) -> Optional[List[int]]:
    if out is None:
        created = True
        out_list: List[int] = []
    else:
        created = False
        out_list = out
    if input_seq is None:
        return out_list if created else None
    code_units = to_utf16_code_units(input_seq)
    pos = 0
    length = len(code_units)
    while pos < length:
        consumed = self.translate_codepoint(code_units, pos, out_list)
        if consumed == 0:
            codepoint = code_point_at(code_units, pos)
            c = to_chars(codepoint)
            out_list.extend(c)
            pos += len(c)
            continue
        for _ in range(consumed):
            pos += char_count(code_point_at(code_units, pos))
    return out_list if created else None