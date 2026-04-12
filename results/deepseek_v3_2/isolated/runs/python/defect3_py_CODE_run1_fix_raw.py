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
            
            # consumed > 0: translator handled some codepoints
            # Advance pos by the number of code units consumed
            # Since consumed is number of codepoints, we need to convert to code units
            # by iterating over the codepoints.
            # But note: translate_codepoint returns number of codepoints consumed,
            # not code units. So we need to advance pos by the total code units
            # for those codepoints.
            # We can step through each codepoint.
            for _ in range(consumed):
                # Get the codepoint at current pos (which is in code units)
                cp = code_point_at(code_units, pos)
                pos += char_count(cp)
            # After loop, pos is correctly advanced.
        