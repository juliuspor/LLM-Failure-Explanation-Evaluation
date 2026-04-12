@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # Normalize bounds
    if lower < 0:
        lower = 0
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # If the text is already shorter or equal to upper, no abbreviation needed
    if text_len <= upper:
        return text

    # Find space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    # If no space found or space beyond upper, cut at upper
    if index == -1 or index > upper:
        result = substring_java(text, 0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # Found space within bounds
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)