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
            
            # Move pos forward by the number of code units consumed
            # consumed is the number of code units, not codepoints.
            # However, translate_codepoint returns the number of codepoints consumed.
            # We need to convert that to code units.
            # We'll iterate over the consumed codepoints and sum their charCounts.
            total_code_units = 0
            for _ in range(consumed):
                cp = code_point_at(code_units, pos + total_code_units)
                total_code_units += char_count(cp)
            pos += total_code_units