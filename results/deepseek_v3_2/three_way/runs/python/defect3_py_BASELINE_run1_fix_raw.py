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
                pos += len(c)
                continue
            # consumed > 0: translator handled 'consumed' codepoints
            # Compute how many UTF-16 code units those codepoints occupy
            temp_pos = pos
            total_code_units = 0
            for _ in range(consumed):
                if temp_pos >= length:
                    break
                codepoint = code_point_at(code_units, temp_pos)
                units = char_count(codepoint)
                total_code_units += units
                temp_pos += units
            pos += total_code_units