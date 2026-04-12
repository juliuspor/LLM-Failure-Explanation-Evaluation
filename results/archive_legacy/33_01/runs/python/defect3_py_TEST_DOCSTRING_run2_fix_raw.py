def translate(self, input_seq: Optional[str], out: Optional[List[int]]) -> Optional[str]:
    if out is None:
        temp_out: List[int] = []
        self._translate_internal(input_seq, temp_out)
        result_chars = []
        i = 0
        while i < len(temp_out):
            if 0xD800 <= temp_out[i] <= 0xDBFF and i + 1 < len(temp_out):
                if 0xDC00 <= temp_out[i + 1] <= 0xDFFF:
                    codepoint = 0x10000 + ((temp_out[i] - 0xD800) << 10) + (temp_out[i + 1] - 0xDC00)
                    result_chars.append(chr(codepoint))
                    i += 2
                    continue
            result_chars.append(chr(temp_out[i]))
            i += 1
        return ''.join(result_chars)
    else:
        self._translate_internal(input_seq, out)
        return None

def _translate_internal(self, input_seq: Optional[str], out: List[int]) -> None:
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
            codepoint = code_point_at(code_units, pos)
            c = to_chars(codepoint)
            out.extend(c)
            pos += len(c)
            continue
        for pt in range(consumed):
            pos += char_count(code_point_at(code_units, pos))