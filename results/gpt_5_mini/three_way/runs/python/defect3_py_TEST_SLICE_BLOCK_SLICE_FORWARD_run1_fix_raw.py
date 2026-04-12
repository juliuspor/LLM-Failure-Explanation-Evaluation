def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return

    # Work with Python string code points (one per character in Python)
    codepoints = [ord(ch) for ch in input_seq]

    pos = 0
    length = len(codepoints)

    while pos < length:
        consumed = self.translate_codepoint(codepoints, pos, out)
        if consumed == 0:
            # No translation; write the current codepoint as UTF-16 code units
            cp = codepoints[pos]
            out.extend(to_chars(cp))
            pos += 1
            continue

        # If translator consumed n codepoints, advance pos by that many
        pos += consumed
