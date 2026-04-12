def code_point_at(code_units: List[int], index: int) -> int:
    """
    Get the Unicode codepoint at the given index in a list of UTF-16 code units.
    Equivalent to Java's Character.codePointAt().
    
    Raises:
        IndexError: if index is out of range
    """
    if index < 0 or index > len(code_units) - 1:
        raise IndexError(f"String index out of range: {index}")
    
    high = code_units[index]
    if 0xD800 <= high <= 0xDBFF and index + 1 < len(code_units):
        low = code_units[index + 1]
        if 0xDC00 <= low <= 0xDFFF:
            # Valid surrogate pair
            return 0x10000 + ((high - 0xD800) << 10) + (low - 0xDC00)
    return high