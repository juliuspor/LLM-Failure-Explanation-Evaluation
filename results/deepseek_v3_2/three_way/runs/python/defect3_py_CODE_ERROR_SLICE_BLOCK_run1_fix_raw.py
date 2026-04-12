    def translate(self, input_seq: Optional[str], out: List[int]) -> None:
        if out is None:
            raise ValueError("The Writer must not be None")
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
            # consumed is number of code points processed
            # compute total code units consumed
            total_code_units = 0
            temp_pos = pos
            for _ in range(consumed):
                if temp_pos >= length:
                    break
                codepoint = code_point_at(code_units, temp_pos)
                total_code_units += char_count(codepoint)
                temp_pos += char_count(codepoint)
            pos += total_code_units