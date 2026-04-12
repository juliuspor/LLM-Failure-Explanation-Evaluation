def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if input_seq is None:
        return

    # If out is None, create a temporary list to collect output
    temp_out = None
    if out is None:
        temp_out = []
        out_ref = temp_out
    else:
        out_ref = out

    # Convert to UTF-16 code units (simulating Java's char[])
    code_units = to_utf16_code_units(input_seq)

    pos = 0
    length = len(code_units)

    while pos < length:
        consumed = self.translate_codepoint(code_units, pos, out_ref)
        if consumed == 0:
            # Get the codepoint at current position
            codepoint = code_point_at(code_units, pos)
            c = to_chars(codepoint)
            out_ref.extend(c)
            pos += len(c)
            continue

        # Contract with translators is that they have to understand codepoints
        # and they just took care of a surrogate pair
        for pt in range(consumed):
            pos += char_count(code_point_at(code_units, pos))

    # If we used a temporary out, we don't need to do anything further
    return None