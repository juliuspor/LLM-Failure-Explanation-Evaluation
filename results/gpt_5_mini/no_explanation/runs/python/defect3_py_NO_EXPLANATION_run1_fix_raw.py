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
            # No translator handled this position; copy the codepoint as-is
            codepoint = code_point_at(code_units, pos)
            chars = to_chars(codepoint)
            out.extend(chars)
            pos += len(chars)
            continue

        # Validate consumed
        if consumed < 0:
            raise ValueError(f"translate_codepoint returned negative value: {consumed}")

        # Advance pos by the number of codepoints consumed
        for _ in range(consumed):
            if pos >= length:
                # Defensive: nothing more to advance
                break
            cp = code_point_at(code_units, pos)
            pos += char_count(cp)
