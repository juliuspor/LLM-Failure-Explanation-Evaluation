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
            
            # consumed > 0: translator already appended output
            # Move pos forward by the number of code units consumed
            # Since consumed is the number of codepoints, we need to convert to code units
            # However, the contract of translate_codepoint is that it returns codepoints consumed,
            # not code units. So we need to advance by the code units of those codepoints.
            # We can step through each consumed codepoint.
            for _ in range(consumed):
                # Get the codepoint at current pos (which is the start of a codepoint)
                codepoint = code_point_at(code_units, pos)
                pos += char_count(codepoint)
