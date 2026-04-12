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
                pos += len(c)
                continue
            # consumed > 0: translator already appended to out.
            # Need to advance pos by the number of UTF-16 code units of the consumed codepoint(s).
            # consumed is the number of codepoints consumed, not code units.
            # We must advance pos by the total code units of those consumed codepoints.
            # We can step through each consumed codepoint, but we must ensure we don't exceed length.
            # However, the translator's contract is that it consumed exactly 'consumed' codepoints starting at pos.
            # So we can iterate over each consumed codepoint and add its charCount.
            # But we must be careful not to call code_point_at with an index that is in the middle of a surrogate pair.
            # Since we know the translator consumed valid codepoints, we can safely advance.
            # We'll use a temporary index to walk forward.
            temp_pos = pos
            for _ in range(consumed):
                if temp_pos >= length:
                    # Should not happen if translator is correct, but guard.
                    break
                codepoint = code_point_at(code_units, temp_pos)
                temp_pos += char_count(codepoint)
            # Now temp_pos is the new position after consuming 'consumed' codepoints.
            pos = temp_pos