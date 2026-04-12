def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return
    codepoints = [ord(ch) for ch in input_seq]
    pos = 0
    length = len(codepoints)
    while pos < length:
        consumed = self.translate_codepoint(codepoints, pos, out)
        if consumed == 0:
            out.append(codepoints[pos])
            pos += 1
            continue
        pos += consumed