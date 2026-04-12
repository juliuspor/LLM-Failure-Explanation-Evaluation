def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return

    # Convert to UTF-16 code units (simulating Java's char[])
    utf16 = to_utf16_code_units(input_seq)

    pos = 0
    length = len(utf16)

    while pos < length:
        consumed = self.translate_codepoint(utf16, pos, out)
        if consumed == 0:
            # Get the codepoint at current position
            codepoint = code_point_at(utf16, pos)
            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue

        # Contract with translators is that they have to understand codepoints
        # and they just took care of a surrogate pair
        for _ in range(consumed):
            # advance by the number of UTF-16 code units for the codepoint at pos
            pos += char_count(code_point_at(utf16, pos))
