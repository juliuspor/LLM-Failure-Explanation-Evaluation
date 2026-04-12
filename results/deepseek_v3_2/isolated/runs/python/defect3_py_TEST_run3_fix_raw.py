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
                # Advance by the number of code units (not codepoints) that correspond to the codepoint
                # Since we already have the code units in 'c', we can use its length.
                # But we need to advance pos by the number of code units consumed from the input.
                # The input code_units list is in UTF-16, so a surrogate pair is two code units.
                # The function char_count(codepoint) returns 1 for BMP, 2 for supplementary.
                pos += char_count(codepoint)
                continue
            
            # Contract with translators is that they have to understand codepoints
            # and they just took care of a surrogate pair
            # However, the consumed value is the number of codepoints, not code units.
            # We need to convert consumed codepoints to code units.
            # We'll iterate over each consumed codepoint and advance pos accordingly.
            for _ in range(consumed):
                # Get the codepoint at current pos to know how many code units it occupies
                cp = code_point_at(code_units, pos)
                pos += char_count(cp)