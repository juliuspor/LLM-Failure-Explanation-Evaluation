@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # Normalize upper: -1 means no limit -> set to text length
    if upper == -1 or upper > text_len:
        upper = text_len
    # Ensure upper is at least lower and within bounds
    if upper < lower:
        upper = lower
    if upper < 0:
        upper = 0

    index = StringUtils.index_of(text, " ", lower)
    # If no space found
    if index == -1:
        # Use clamped upper (<= text_len)
        result = substring_java(text, 0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # If the first space after lower is beyond upper, cut at upper
    if index > upper:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # Otherwise, cut at the space
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)