def translate(self, input_seq: Optional[str], out: List[int]) -> None:
    if out is None:
        raise ValueError("The Writer must not be null")
    if input_seq is None:
        return
    code_units = to_utf16_code_units(input_seq)
    pos = 0
    length = len(code_units)
    def _safe_codepoint_at(idx: int) -> int:
        if idx < 0 or idx >= length:
            raise IndexError(f"String index out of range: {idx}")
        high = code_units[idx]
        if 0xD800 <= high <= 0xDBFF and idx + 1 < length:
            low = code_units[idx + 1]
            if 0xDC00 <= low <= 0xDFFF:
                return 0x10000 + ((high - 0xD800) << 10) + (low - 0xDC00)
        return high
    while pos < length:
        consumed = self.translate_codepoint(code_units, pos, out)
        if consumed == 0:
            cp = _safe_codepoint_at(pos)
            chars = to_chars(cp)
            out.extend(chars)
            pos += len(chars)
            continue
        for _ in range(consumed):
            cp = _safe_codepoint_at(pos)
            pos += char_count(cp)