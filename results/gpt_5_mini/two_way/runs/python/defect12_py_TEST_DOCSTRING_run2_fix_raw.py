@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # Treat -1 as no limit
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # If lower is beyond the text length, return original text
    if lower >= text_len:
        return text

    # Search for space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    # If no space found or space is beyond upper, cut at upper
    if index == -1 or index > upper:
        end = upper if upper <= text_len else text_len
        result = substring_java(text, 0, end)
        if end < text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # Found space within bounds
    result = substring_java(text, 0, index)
    if index < text_len:
        result += StringUtils.default_string(append_to_end)
    return result