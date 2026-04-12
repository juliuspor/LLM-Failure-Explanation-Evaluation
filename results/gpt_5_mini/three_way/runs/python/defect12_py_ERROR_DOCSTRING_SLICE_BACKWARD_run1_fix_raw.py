@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # Interpret -1 as no limit
    if upper == -1:
        upper = text_len
    # Clamp upper to text length
    if upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # Ensure lower is non-negative
    if lower < 0:
        lower = 0

    index = StringUtils.index_of(text, " ", lower)
    # If no space found at or after lower, just cut at upper
    if index == -1:
        result = substring_java(text, 0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # If the first space found is after the upper bound, cut at upper
    if index > upper:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # Otherwise cut at the space
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)