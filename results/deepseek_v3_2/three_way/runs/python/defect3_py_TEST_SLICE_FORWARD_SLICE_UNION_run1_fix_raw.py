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
                # Advance by the number of code units consumed for this codepoint
                pos += char_count(codepoint)
            else:
                # Contract with translators is that they have to understand codepoints
                # and they just took care of a surrogate pair
                # We need to advance by the number of code units corresponding to the consumed codepoints
                # consumed is the number of codepoints consumed, not code units.
                # We must convert consumed codepoints to code units.
                # Iterate over each consumed codepoint and add its char count.
                total_code_units = 0
                for i in range(consumed):
                    # Get the codepoint at the current position (pos + total_code_units)
                    cp = code_point_at(code_units, pos + total_code_units)
                    total_code_units += char_count(cp)
                pos += total_code_units
