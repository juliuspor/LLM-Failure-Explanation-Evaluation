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
                        # It's a surrogate pair, copy both code units
                        out.append(code_units[pos])
                        out.append(code_units[pos + 1])
                        pos += 2
                        continue
                # Single code unit (BMP or unpaired surrogate)
                out.append(code_units[pos])
                pos += 1
            else:
                # Translator consumed some code units; advance pos by consumed count
                # consumed is number of code units, not codepoints? Actually the contract says codepoints consumed.
                # But the translator works on code units, and we need to advance by code units.
                # The translator's consumed should be the number of code units consumed.
                # However, the abstract method's doc says "number of codepoints consumed", but the implementation in CsvEscaper returns 2 for surrogate pair (code units).
                # To maintain compatibility, we assume consumed is number of code units consumed.
                # The original code attempted to convert consumed codepoints to code units, which is complex.
                # Since the translator works on code units, we can just add consumed to pos.
                pos += consumed
