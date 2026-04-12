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
                # No translation - copy current codepoint as-is
                if pos >= length:
                    break
                codepoint = code_point_at(code_units, pos)
                c = to_chars(codepoint)
                out.extend(c)
                pos += len(c)
                continue
            
            # Advance by total UTF-16 code units for consumed codepoints
            # Use conservative estimate: each codepoint is at most 2 code units
            pos += min(consumed * 2, length - pos)
            
            # Fine-tune: backtrack if we overshot
            while pos > length:
                pos = length
            
            # Ensure we don't get stuck
            if pos == 0:
                pos = 1
            
            # Skip any remaining code units that belong to consumed codepoints
            while pos < length:
                next_cp = code_point_at(code_units, pos)
                cu_count = char_count(next_cp)
                if pos + cu_count > length:
                    break
                pos += cu_count
                consumed -= 1
                if consumed <= 0:
                    break

        # Ensure we process any remaining characters
        while pos < length:
            consumed = self.translate_codepoint(code_units, pos, out)
            if consumed == 0:
                codepoint = code_point_at(code_units, pos)
                c = to_chars(codepoint)
                out.extend(c)
                pos += len(c)
            else:
                pos += min(consumed * 2, length - pos)
                break
