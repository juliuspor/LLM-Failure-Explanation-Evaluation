    def translate(self, input_seq: Optional[str], out: List[int]) -> None:
        """
        Translate `input_seq` into UTF-16 code units appended to `out`.

        Subclasses customize behavior by implementing `translate_codepoint()`,
        which can consume one or more code points at the current position.

        Args:
            input_seq: Text to translate. If None, nothing is written.
            out: Destination list of UTF-16 code units.
            
        Raises:
            ValueError: If `out` is None.
        """
        if out is None:
            raise ValueError("The Writer must not be null")
        if input_seq is None:
            return
        
        # Convert to UTF-16 code units (simulating Java's char[])
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
                pos += char_count(codepoint)
                continue
            
            # Contract with translators is that they have to understand codepoints
            # and they just took care of a surrogate pair
            # We need to advance pos by the number of code units consumed?
            # Actually, consumed is the number of codepoints consumed, not code units.
            # So we need to advance pos by the number of code units corresponding to those codepoints.
            # The original code looped over pt in range(consumed) and added char_count for each codepoint.
            # That is correct, but we must ensure we don't exceed length.
            # However, the loop variable pt is not used; we just need to advance pos by the total code units.
            # Let's compute total code units for the consumed codepoints.
            # But we don't have the exact codepoints? We can iterate from current pos.
            # The original implementation: for pt in range(consumed): pos += char_count(code_point_at(code_units, pos))
            # This works because each iteration reads the codepoint at the current pos (which advances).
            # However, note that after the first iteration, the index pos has moved, so code_point_at uses new pos.
            # That is correct: we are consuming codepoints sequentially.
            # We'll keep the original loop.
            for pt in range(consumed):
                pos += char_count(code_point_at(code_units, pos))
