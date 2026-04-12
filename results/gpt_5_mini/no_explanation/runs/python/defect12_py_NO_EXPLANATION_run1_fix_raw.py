@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    if upper == -1 or upper > text_len:
        upper = text_len
    if lower < 0:
        lower = 0
    if upper < lower:
        upper = lower

    # Find the first space at or after lower
    index = text.find(" ", lower)
    # If no space found or space is beyond upper, cut at upper
    if index == -1 or index > upper:
        # If upper equals the full length, no abbreviation needed
        if upper >= text_len:
            return text
        result = substring_java(text, 0, upper)
        return result + StringUtils.default_string(append_to_end)

    # Found a space within bounds: cut at that space
    if index <= 0:
        # nothing before the space
        return StringUtils.default_string(append_to_end) if upper < text_len else text

    result = substring_java(text, 0, index)
    if index < text_len:
        result += StringUtils.default_string(append_to_end)
    return result