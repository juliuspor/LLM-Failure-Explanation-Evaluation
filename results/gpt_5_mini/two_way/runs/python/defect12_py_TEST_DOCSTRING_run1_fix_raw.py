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
    if upper == -1:
        upper = text_len

    # Normalize bounds
    if lower < 0:
        lower = 0
    if upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # If lower is beyond text length, return original text
    if lower >= text_len:
        return text

    # Find space at or after lower
    index = StringUtils.index_of(text, " ", lower)

    # No space found -> cut at upper
    if index == -1:
        # If upper is at or beyond end, return original
        if upper >= text_len:
            return text
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # Space found after upper -> cut at upper
    if index > upper:
        if upper >= text_len:
            return text
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # Cut at the space
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)