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
                # Advance by the number of code units (chars) that represent the codepoint
                pos += char_count(codepoint)
            else:
                # consumed is the number of codepoints consumed, not code units.
                # Need to advance pos by the total code units for those codepoints.
                # Since we don't know exactly which codepoints were consumed, we must
                # iterate through each consumed codepoint and add its char count.
                # However, the contract of translate_codepoint is that it returns the
                # number of codepoints consumed, and it must have processed exactly
                # those codepoints starting at pos. So we can step through each codepoint.
                remaining = consumed
                i = pos
                while remaining > 0:
                    cp = code_point_at(code_units, i)
                    i += char_count(cp)
                    remaining -= 1
                pos = i
