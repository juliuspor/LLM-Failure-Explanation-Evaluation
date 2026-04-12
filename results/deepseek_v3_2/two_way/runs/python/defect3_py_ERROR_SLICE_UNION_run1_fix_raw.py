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
            else:
                # consumed is the number of codepoints consumed, not code units.
                # Need to advance pos by the total code units of those codepoints.
                # We must iterate over each consumed codepoint and add its charCount.
                # However, we don't have the codepoints directly; we can compute them
                # from the code_units list starting at pos.
                # But note: the translator already wrote the translation to out,
                # and consumed tells how many codepoints were consumed from input.
                # We need to advance pos by the total code units of those codepoints.
                # We can step through each codepoint:
                i = 0
                for _ in range(consumed):
                    # Get codepoint at current position (pos + i)
                    cp = code_point_at(code_units, pos + i)
                    i += char_count(cp)
                pos += i
