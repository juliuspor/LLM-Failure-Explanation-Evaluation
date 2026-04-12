def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return

    # Convert to code points (one entry per Unicode codepoint)
    codepoints = [ord(ch) for ch in input_seq]

    pos = 0
    length = len(codepoints)

    while pos < length:
        consumed = self.translate_codepoint(codepoints, pos, out)
        if consumed == 0:
            cp = codepoints[pos]
            c = to_chars(cp)
            out.extend(c)
            pos += 1
            continue

        for _ in range(consumed):
            # Each consumed item is one codepoint, so advance by 1 per consumed
            pos += 1
