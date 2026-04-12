def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return

    # Convert to UTF-16 code units (simulating Java's char[])
    code_units = to_utf16_code_units(input_seq)

    # Build mapping from Python string index (code point index) to UTF-16 code unit index
    cp_to_cu = []  # cp_to_cu[i] = index into code_units where python char i starts
    cu_index = 0
    for ch in input_seq:
        cp_to_cu.append(cu_index)
        cp = ord(ch)
        cu_index += char_count(cp)

    pos = 0
    length = len(input_seq)  # iterate over Python code points (string indices)

    while pos < length:
        cu_pos = cp_to_cu[pos]
        consumed = self.translate_codepoint(code_units, cu_pos, out)
        if consumed == 0:
            # No translator consumed codepoints; write the original codepoint
            codepoint = ord(input_seq[pos])
            c = to_chars(codepoint)
            out.extend(c)
            pos += 1
            continue

        # consumed is in codepoints; advance pos by that many code points
        pos += consumed
