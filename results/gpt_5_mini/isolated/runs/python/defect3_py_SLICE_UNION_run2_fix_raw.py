def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return

    # Convert to UTF-16 code units (simulating Java's char[])
    # Ensure code_units is properly populated even if to_utf16_code_units were faulty
    code_units: List[int] = []
    for ch in input_seq:
        cp = ord(ch)
        if cp > 0xFFFF:
            cp -= 0x10000
            high = 0xD800 + (cp >> 10)
            low = 0xDC00 + (cp & 0x3FF)
            code_units.append(high)
            code_units.append(low)
        else:
            code_units.append(cp)

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

        # Contract with translators is that they have to understand codepoints
        # and they just took care of a surrogate pair
        for pt in range(consumed):
            pos += char_count(code_point_at(code_units, pos))