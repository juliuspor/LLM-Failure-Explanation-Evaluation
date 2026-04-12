    def translate_codepoint(self, code_units: List[int], index: int, out: List[int]) -> int:
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
                pos += len(c)
                continue
            
            # Contract with translators is that they have to understand codepoints
            # and they just took care of a surrogate pair
            for pt in range(consumed):
                pos += char_count(code_point_at(code_units, pos))

    def translate_codepoint(self, code_units: List[int], index: int, out: List[int]) -> int:
        """
        Escape CSV special characters.
        Returns the number of codepoints consumed.
        """
        code_unit = code_units[index]
        
        # Check if this is a high surrogate (start of surrogate pair)
        if 0xD800 <= code_unit <= 0xDBFF and index + 1 < len(code_units):
            low = code_units[index + 1]
            if 0xDC00 <= low <= 0xDFFF:
                # Valid surrogate pair - write both code units
                out.append(code_unit)
                out.append(low)
                return 2
        
        # Handle quote escaping: " -> ""
        if code_unit == ord('"'):
            out.append(ord('"'))
            out.append(ord('"'))
            return 1
        
        # No translation needed for other characters
        return 0
