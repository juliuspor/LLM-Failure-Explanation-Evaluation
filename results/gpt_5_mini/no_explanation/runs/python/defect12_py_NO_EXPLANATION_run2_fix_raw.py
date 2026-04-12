@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # Normalize upper: -1 means no limit
    if upper == -1 or upper > text_len:
        upper = text_len
    if lower < 0:
        lower = 0
    if upper < lower:
        upper = lower

    # If lower is at or beyond text length, nothing to abbreviate
    if lower >= text_len:
        return text if upper >= text_len else substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # Find first space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    # No space found
    if index == -1 or index > upper:
        # If upper is at the end, return original text
        if upper >= text_len:
            return text
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # Found space within bounds
    # If the space is at position 0, return empty + append
    if index == 0:
        return StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)