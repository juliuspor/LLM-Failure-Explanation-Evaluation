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
                codepoint = code_point_at(code_units, pos)
                c = to_chars(codepoint)
                out.extend(c)
                pos += len(c)
            else:
                # Advance by the number of UTF-16 code units consumed
                # For surrogate pairs, consumed=2 means 2 code units
                pos += consumed
                
                # Additional safety: ensure we don't overshoot
                if pos > length:
                    pos = length
                
                # Skip any remaining code units for multi-codepoint sequences
                # by advancing to next full codepoint boundary
                while pos < length and (0xD800 <= code_units[pos] <= 0xDBFF):
                    pos += 1
                    if pos < length and 0xDC00 <= code_units[pos] <= 0xDFFF:
                        pos += 1
                    break
                
                # Ensure we don't go beyond length
                pos = min(pos, length)