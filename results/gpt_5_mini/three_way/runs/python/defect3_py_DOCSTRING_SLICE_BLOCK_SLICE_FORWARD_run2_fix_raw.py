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
            # Advance pos by the number of UTF-16 code units that correspond
            # to the consumed code points, guarding against over-consumption.
            temp_pos = pos
            for _ in range(consumed):
                if temp_pos >= length:
                    break
                cp = code_point_at(code_units, temp_pos)
                temp_pos += char_count(cp)
            # Ensure we always make progress; if translator lied and didn't
            # consume anything real, avoid infinite loop by advancing by 1.
            if temp_pos == pos:
                pos += 1
            else:
                pos = temp_pos