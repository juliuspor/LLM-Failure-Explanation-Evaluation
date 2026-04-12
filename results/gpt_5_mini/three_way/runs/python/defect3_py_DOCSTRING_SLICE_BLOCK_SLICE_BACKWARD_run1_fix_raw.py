def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return

    code_units = to_utf16_code_units(input_seq)

    pos = 0
    length = len(code_units)

    while pos < length:
        # Ask translator how many code points it consumes at this UTF-16 index
        consumed = self.translate_codepoint(code_units, pos, out)
        if consumed == 0:
            # No translation; copy the codepoint at pos
            codepoint = code_point_at(code_units, pos)
            chars = to_chars(codepoint)
            out.extend(chars)
            pos += len(chars)
            continue

        # Translator consumed 'consumed' Unicode code points starting at pos.
        # Advance pos by the number of UTF-16 code units those code points occupy.
        for _ in range(consumed):
            # Ensure pos is still within bounds before reading
            if pos >= length:
                break
            cp = code_point_at(code_units, pos)
            pos += char_count(cp)