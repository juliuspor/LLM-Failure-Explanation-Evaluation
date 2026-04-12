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
            # Determine if current unit starts a valid surrogate pair
            unit = code_units[pos]
            if 0xD800 <= unit <= 0xDBFF and pos + 1 < length and 0xDC00 <= code_units[pos + 1] <= 0xDFFF:
                out.append(unit)
                out.append(code_units[pos + 1])
                pos += 2
            else:
                out.append(unit)
                pos += 1
            continue

        # consumed indicates number of Unicode code points consumed; for each,
        # advance pos by the number of UTF-16 code units that represent it
        for _ in range(consumed):
            if pos >= length:
                break
            unit = code_units[pos]
            if 0xD800 <= unit <= 0xDBFF and pos + 1 < length and 0xDC00 <= code_units[pos + 1] <= 0xDFFF:
                pos += 2
            else:
                pos += 1
