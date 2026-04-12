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
                # Advance by the number of code units this codepoint occupies
                pos += char_count(codepoint)
                continue
            
            # Contract with translators is that they have to understand codepoints
            # and they just took care of a surrogate pair
            # We need to advance pos by the number of code units consumed.
            # consumed is the number of codepoints, not code units.
            # So we must convert consumed codepoints to code units.
            # We'll iterate over each consumed codepoint and add its charCount.
            for _ in range(consumed):
                # Get the codepoint at current pos (which may be a surrogate pair)
                cp = code_point_at(code_units, pos)
                pos += char_count(cp)
