def translate_codepoint(self, code_units: List[int], index: int, out: List[int]) -> int:
    if index >= len(code_units):
        return 0
    """
    Translate a set of codepoints, represented by an int index into a list of code units,
    into another set of codepoints. The number of codepoints consumed must be returned.
    
    Args:
        code_units: List of UTF-16 code units being translated
        index: int representing the current point of translation
        out: List to append translated code units to
        
    Returns:
        int count of codepoints consumed
    """
    pass


def translate_codepoint(self, code_units: List[int], index: int, out: List[int]) -> int:
    if index >= len(code_units):
        return 0
    """
    Escape CSV special characters.
    Returns the number of codepoints consumed.
    """
    code_unit = code_units[index]
    
    # Check if this is a high surrogate (start of surrogate pair)
    if 0xD800 <= code_unit <= 0xDBFF:
        if index + 1 < len(code_units):
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

def translate_codepoint(self, code_units: List[int], index: int, out: List[int]) -> int:
    if index >= len(code_units):
        return 0
    for translator in self._translators:
        consumed = translator.translate_codepoint(code_units, index, out)
        if consumed != 0:
            return consumed
    return 0