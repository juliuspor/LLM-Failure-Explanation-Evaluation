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
            else:
                # Contract with translators is that they have to understand codepoints
                # and they just took care of a surrogate pair
                # We need to advance pos by the number of code units consumed, not codepoints.
                # The consumed value is the number of codepoints consumed.
                # We must convert that to code units.
                # However, the translator's translate_codepoint returns codepoints consumed,
                # but the code units consumed may be more (if surrogate pairs).
                # We need to advance pos by the number of code units corresponding to the consumed codepoints.
                # We can iterate through the consumed codepoints and sum their charCount.
                # Alternatively, we can compute the total code units consumed by the translator.
                # Since the translator already wrote to out, we need to know how many code units it consumed.
                # The current implementation incorrectly uses charCount on the codepoint at pos, which may be wrong.
                # Let's fix by advancing pos by the number of code units that correspond to the consumed codepoints.
                # We'll compute by scanning the code units from pos forward, counting codepoints until we reach consumed.
                remaining = consumed
                i = pos
                while remaining > 0 and i < length:
                    cp = code_point_at(code_units, i)
                    i += char_count(cp)
                    remaining -= 1
                pos = i
