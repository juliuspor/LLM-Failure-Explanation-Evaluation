def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return
    code_units = to_utf16_code_units(input_seq)
    char_to_cu = []
    cu_index = 0
    for ch in input_seq:
        char_to_cu.append(cu_index)
        cp = ord(ch)
        cu_index += 2 if cp > 0xFFFF else 1
    pos_char = 0
    length_chars = len(input_seq)
    while pos_char < length_chars:
        cu_idx = char_to_cu[pos_char]
        consumed = self.translate_codepoint(code_units, cu_idx, out)
        if consumed == 0:
            high = ord(input_seq[pos_char])
            if 0xD800 <= high <= 0xDBFF and pos_char + 1 < length_chars:
                low = ord(input_seq[pos_char + 1])
                if 0xDC00 <= low <= 0xDFFF:
                    codepoint = 0x10000 + ((high - 0xD800) << 10) + (low - 0xDC00)
                    out.extend(to_chars(codepoint))
                    pos_char += 2
                    continue
            out.extend(to_chars(high))
            pos_char += 1
            continue
        pos_char += consumed
    return None