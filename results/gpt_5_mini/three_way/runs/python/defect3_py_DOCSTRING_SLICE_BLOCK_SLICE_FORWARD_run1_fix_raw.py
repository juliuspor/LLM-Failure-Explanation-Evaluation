def translate(self, input_seq: Optional[str], out: list) -> None:
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

            # If codepoint is a high surrogate value (unpaired), detect and raise
            if 0xD800 <= codepoint <= 0xDBFF:
                # If there's no following low surrogate, this is an unpaired high surrogate
                if pos + 1 >= length or not (0xDC00 <= code_units[pos + 1] <= 0xDFFF):
                    raise ValueError(f"Unpaired high surrogate at index {pos}, input length {length}")

            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue

        for pt in range(consumed):
            pos += char_count(code_point_at(code_units, pos))
