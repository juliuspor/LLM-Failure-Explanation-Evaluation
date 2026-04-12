def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return

    # Convert to UTF-16 code units (simulating Java's char[])
    code_units = to_utf16_code_units(input_seq)

    pos = 0
    length = len(code_units)

    while pos < length:
        consumed = self.translate_codepoint(code_units, pos, out)
        if consumed == 0:
            # No translator handled this position; copy the current code unit(s)
            cu = code_units[pos]
            # If this is a high surrogate and next is a low surrogate, copy both
            if 0xD800 <= cu <= 0xDBFF and pos + 1 < length and 0xDC00 <= code_units[pos + 1] <= 0xDFFF:
                out.append(cu)
                out.append(code_units[pos + 1])
                pos += 2
            else:
                out.append(cu)
                pos += 1
            continue

        # The translator reports how many UTF-16 code units it consumed; advance by that many
        pos += consumed
