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
            
            # Advance pos by the total number of code units corresponding to the consumed codepoints
            total_code_units = 0
            for _ in range(consumed):
                codepoint = code_point_at(code_units, pos + total_code_units)
                total_code_units += char_count(codepoint)
            pos += total_code_units