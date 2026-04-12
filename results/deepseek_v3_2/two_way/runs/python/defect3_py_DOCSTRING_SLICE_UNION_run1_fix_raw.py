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
                codepoint = code_point_at(code_units, pos)
                c = to_chars(codepoint)
                out.extend(c)
                pos += char_count(codepoint)
                continue
            # consumed is number of codepoints consumed
            # convert that to number of code units
            code_unit_consumed = 0
            for i in range(consumed):
                cp = code_point_at(code_units, pos + code_unit_consumed)
                code_unit_consumed += char_count(cp)
            pos += code_unit_consumed