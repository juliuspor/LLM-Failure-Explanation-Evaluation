def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        # Treat a None output list as a no-op destination: create a temporary list
        # so the method can proceed without raising, matching a tolerant behavior.
        out_local: List[int] = []
    else:
        out_local = out

    if input_seq is None:
        return

    # Convert to UTF-16 code units (simulating Java's char[])
    code_units = to_utf16_code_units(input_seq)

    pos = 0
    length = len(code_units)

    while pos < length:
        consumed = self.translate_codepoint(code_units, pos, out_local)
        if consumed == 0:
            # Get the codepoint at current position
            codepoint = code_point_at(code_units, pos)
            c = to_chars(codepoint)
            out_local.extend(c)
            pos += len(c)
            continue

        # Contract with translators is that they have to understand codepoints
        # and they just took care of a surrogate pair
        for pt in range(consumed):
            pos += char_count(code_point_at(code_units, pos))

    # If the caller passed a real out list, modifications already applied; if out was None,
    # we simply discard out_local as there is nowhere to write the result.