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
                # No translation, copy the current codepoint
                codepoint = code_point_at(code_units, pos)
                c = to_chars(codepoint)
                out.extend(c)
                # Advance by the number of code units in the codepoint
                pos += char_count(codepoint)
            else:
                # The translator consumed 'consumed' codepoints
                # We need to advance pos by the corresponding number of code units
                for _ in range(consumed):
                    codepoint = code_point_at(code_units, pos)
                    pos += char_count(codepoint)
