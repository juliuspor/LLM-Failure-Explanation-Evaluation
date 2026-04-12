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
            cp = codepoints[pos]
            if cp > 0xFFFF:
                cp_minus = cp - 0x10000
                out.append(0xD800 + (cp_minus >> 10))
                out.append(0xDC00 + (cp_minus & 0x3FF))
            else:
                out.append(cp)
            pos += 1
            continue
        pos += consumed
    return None