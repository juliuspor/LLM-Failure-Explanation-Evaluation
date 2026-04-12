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
                # No translation, copy the current code unit(s)
                # Determine if current position is a high surrogate start of a pair
                if 0xD800 <= code_units[pos] <= 0xDBFF and pos + 1 < length:
                    low = code_units[pos + 1]
                    if 0xDC00 <= low <= 0xDFFF:
                        # Valid surrogate pair
                        out.append(code_units[pos])
                        out.append(code_units[pos + 1])
                        pos += 2
                        continue
                # Single code unit (BMP or unpaired surrogate)
                out.append(code_units[pos])
                pos += 1
                continue
            
            # consumed > 0: translator processed 'consumed' codepoints
            # Need to advance pos by the number of UTF-16 code units those codepoints occupy
            for _ in range(consumed):
                # Get the codepoint at current pos (handles surrogate pairs)
                codepoint = code_point_at(code_units, pos)
                pos += char_count(codepoint)
