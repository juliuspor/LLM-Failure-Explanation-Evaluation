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
                # Advance by the number of code units, not codepoints
                # char_count(codepoint) returns number of code units (1 or 2)
                pos += char_count(codepoint)
                continue
            
            # consumed is the number of codepoints consumed, not code units.
            # Need to convert consumed codepoints to code units.
            # We must advance pos by the total number of code units that correspond to those codepoints.
            # We can iterate through each consumed codepoint and add its charCount.
            # Alternatively, we can compute directly: we know the starting position and we need to skip the consumed codepoints.
            # Since we have the original code_units, we can compute the number of code units that make up the consumed codepoints.
            # Let's step through each codepoint until we have accounted for 'consumed' codepoints.
            remaining = consumed
            i = pos
            while remaining > 0 and i < length:
                cp = code_point_at(code_units, i)
                i += char_count(cp)
                remaining -= 1
            # Now i is the new position after consuming 'consumed' codepoints.
            pos = i
