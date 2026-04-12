def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return
    code_points = [ord(ch) for ch in input_seq]
    pos = 0
    length = len(code_points)
    while pos < length:
        consumed = self.translate_codepoint(code_points, pos, out)
        if consumed == 0:
            codepoint = code_points[pos]
            out.extend(to_chars(codepoint))
            pos += 1
            continue
        pos += consumed