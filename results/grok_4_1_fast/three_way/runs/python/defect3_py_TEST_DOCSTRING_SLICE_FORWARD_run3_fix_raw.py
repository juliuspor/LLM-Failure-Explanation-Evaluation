def code_point_at(code_units: List[int], index: int) -> int:
    """
    Get the Unicode codepoint at the given index in a list of UTF-16 code units.
    Equivalent to Java's Character.codePointAt().
    
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
            return 0x10000 + ((high - 0xD800) << 10) + (low - 0xDC00)
    return high


def char_count(codepoint: int) -> int:
    """
    Returns the number of UTF-16 code units needed to represent a codepoint.
    Equivalent to Java's Character.charCount().
    """
    return 2 if codepoint > 0xFFFF else 1


def to_chars(codepoint: int) -> List[int]:
    """
    Convert a codepoint to UTF-16 code units.
    Equivalent to Java's Character.toChars().
    """
    if codepoint > 0xFFFF:
        codepoint -= 0x10000
        return [0xD800 + (codepoint >> 10), 0xDC00 + (codepoint & 0x3FF)]
    return [codepoint]