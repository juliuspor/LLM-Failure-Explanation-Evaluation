def code_point_at(code_units: List[int], index: int) -> tuple[int, int]:
    """
    Get the Unicode codepoint at the given index in a list of UTF-16 code units,
    and return the number of code units consumed.
    Equivalent to Java's Character.codePointAt().
    
    Returns:
        tuple(codepoint: int, consumed: int)
    
    Raises:
        IndexError: if index is out of range
    """
    if index < 0 or index >= len(code_units):
        raise IndexError(f"String index out of range: {index}")
    
    high = code_units[index]
    if 0xD800 <= high <= 0xDBFF and index + 1 < len(code_units):
        low = code_units[index + 1]
        if 0xDC00 <= low <= 0xDFFF:
            # Valid surrogate pair
            codepoint = 0x10000 + ((high - 0xD800) << 10) + (low - 0xDC00)
            return codepoint, 2
    return high, 1


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
                codepoint, char_count = code_point_at(code_units, pos)
                c = to_chars(codepoint)
                out.extend(c)
                pos += char_count
                continue
            
            # Contract with translators is that they have to understand codepoints
            # and they just took care of a surrogate pair
            for pt in range(consumed):
                _, count = code_point_at(code_units, pos)
                pos += count
