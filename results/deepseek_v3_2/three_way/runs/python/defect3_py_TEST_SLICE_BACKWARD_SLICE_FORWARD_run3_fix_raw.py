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
                # Get the codepoint at current position
                codepoint = code_point_at(code_units, pos)
                c = to_chars(codepoint)
                out.extend(c)
                # Advance by the number of code units consumed, not codepoints
                # char_count(codepoint) returns 1 for BMP, 2 for surrogate pair
                pos += char_count(codepoint)
            else:
                # consumed is number of codepoints consumed, not code units
                # Need to advance pos by the number of code units corresponding to those codepoints
                # We must iterate over each consumed codepoint and add its charCount
                total_code_units = 0
                for _ in range(consumed):
                    cp = code_point_at(code_units, pos + total_code_units)
                    total_code_units += char_count(cp)
                pos += total_code_units
