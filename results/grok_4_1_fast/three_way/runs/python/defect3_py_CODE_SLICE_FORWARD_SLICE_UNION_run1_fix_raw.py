def translate_codepoint(self, code_units: List[int], index: int, out: List[int]) -> int:
    """
    Escape CSV special characters.
    Returns the number of codepoints consumed.
    """
    codepoint = code_point_at(code_units, index)
    
    # Handle quote escaping: " -> ""
    if codepoint == ord('"'):
        out.append(ord('"'))
        out.append(ord('"'))
        return 1
    
    # No translation needed for other characters
    return 0