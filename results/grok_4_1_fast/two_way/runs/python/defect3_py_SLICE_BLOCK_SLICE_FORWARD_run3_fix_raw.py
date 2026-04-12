def code_point_at(code_units: List[int], index: int) -> int:
    """
    Get the Unicode codepoint at the given index in a list of UTF-16 code units.
    Equivalent to Java's Character.codePointAt().
    
    Raises:
        IndexError: if index is out of range
        ValueError: if malformed surrogate pair
    """
    if index < 0 or index >= len(code_units):
        raise IndexError(f"String index out of range: {index}")
    
    high = code_units[index]
    if 0xD800 <= high <= 0xDBFF:
        if index + 1 >= len(code_units):
            raise ValueError("Malformed UTF-16: high surrogate not followed by low surrogate")
        low = code_units[index + 1]
        if 0xDC00 <= low <= 0xDFFF:
            # Valid surrogate pair
            return 0x10000 + ((high - 0xD800) << 10) + (low - 0xDC00)
        else:
            raise ValueError("Malformed UTF-16: high surrogate not followed by valid low surrogate")
    elif 0xDC00 <= high <= 0xDFFF:
        raise ValueError("Malformed UTF-16: stray low surrogate")
    
    return high

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
            # No translation - copy current codepoint
            codepoint = code_point_at(code_units, pos)
            c = to_chars(codepoint)
            out.extend(c)
            pos += char_count(codepoint)
        else:
            # Translator consumed some codepoints - advance accordingly
            for _ in range(consumed):
                codepoint = code_point_at(code_units, pos)
                pos += char_count(codepoint)