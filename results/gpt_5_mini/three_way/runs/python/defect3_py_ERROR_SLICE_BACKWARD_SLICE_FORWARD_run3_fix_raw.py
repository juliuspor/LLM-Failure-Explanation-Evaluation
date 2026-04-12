def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return

    code_units = to_utf16_code_units(input_seq)

    pos = 0
    length = len(code_units)

    while pos < length:
        consumed = self.translate_codepoint(code_units, pos, out)
        if consumed == 0:
            # Get the codepoint at current position
            codepoint = code_point_at(code_units, pos)
            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue

        # consumed is the number of code points consumed; advance pos by the
        # number of UTF-16 code units those code points occupy. Be careful
        # not to read past the end of the code_units list.
        to_advance = 0
        for _ in range(consumed):
            if pos >= length:
                break
            cp = code_point_at(code_units, pos)
            to_advance += char_count(cp)
            pos += char_count(cp)
        # pos already advanced in the loop; ensure we don't overshoot
        if pos > length:
            pos = length
        # continue with next iteration
        continue