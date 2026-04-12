@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)

    # Treat upper == -1 as no limit (use full length)
    if upper == -1:
        upper = text_len

    # Clamp upper to valid range
    if upper > text_len:
        upper = text_len
    if upper < 0:
        upper = 0

    if upper < lower:
        upper = lower

    # If lower is beyond text length, nothing to abbreviate: return original
    if lower >= text_len:
        return text

    # Find first space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # no space found; cut at upper
        # If upper is beyond or equal to length, no truncation
        if upper >= text_len:
            return text
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # If the found space is after upper, cut at upper
    if index > upper:
        if upper >= text_len:
            return text
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # Otherwise cut at the space index
    # If index is 0, return empty + append if truncated
    if index >= text_len:
        return text
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)