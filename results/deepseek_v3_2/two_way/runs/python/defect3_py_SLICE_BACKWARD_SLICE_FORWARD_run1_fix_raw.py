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
        code_units = []
        for char in input_seq:
            codepoint = ord(char)
            if codepoint > 0xFFFF:
                # Encode as surrogate pair (like Java)
                codepoint -= 0x10000
                high = 0xD800 + (codepoint >> 10)
                low = 0xDC00 + (codepoint & 0x3FF)
                code_units.append(high)
                code_units.append(low)
            else:
                code_units.append(codepoint)
        
        pos = 0
        length = len(code_units)
        
        while pos < length:
            consumed = self.translate_codepoint(code_units, pos, out)
            if consumed == 0:
                # Get the codepoint at current position
                codepoint = code_point_at(code_units, pos)
                c = to_chars(codepoint)
                out.extend(c)
                pos += len(c)
                continue
            
            # Contract with translators is that they have to understand codepoints
            # and they just took care of a surrogate pair
            for pt in range(consumed):
                pos += char_count(code_point_at(code_units, pos))