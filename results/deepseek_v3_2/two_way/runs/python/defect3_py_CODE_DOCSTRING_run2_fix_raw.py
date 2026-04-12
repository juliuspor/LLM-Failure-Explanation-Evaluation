    def translate(self, input_seq: Optional[str], out: List[int]) -> None:
        if out is None:
            raise ValueError("The Writer must not be null")
        if input_seq is None:
            return
        
        code_units = to_utf16_code_units(input_seq)
        pos = 0
        length = len(code_units)
        
        while pos < length:
            consumed_codepoints = self.translate_codepoint(code_units, pos, out)
            if consumed_codepoints == 0:
                codepoint = code_point_at(code_units, pos)
                c = to_chars(codepoint)
                out.extend(c)
                pos += len(c)
                continue
            
            # Advance pos by the number of code units corresponding to consumed_codepoints
            # Scan from pos to count code units for exactly consumed_codepoints codepoints
            remaining = consumed_codepoints
            idx = pos
            while remaining > 0 and idx < length:
                cp = code_point_at(code_units, idx)
                idx += char_count(cp)
                remaining -= 1
            if remaining != 0:
                # Should not happen if translator behaves correctly, but fallback
                idx = length
            pos = idx
