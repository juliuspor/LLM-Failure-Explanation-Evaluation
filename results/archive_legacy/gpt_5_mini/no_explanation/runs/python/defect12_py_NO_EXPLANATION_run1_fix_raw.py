@staticmethod
def abbreviate(text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # normalize lower
    if lower < 0:
        lower = 0

    text_len = len(text)
    # normalize upper: -1 means no limit
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # If lower is beyond text length, nothing to abbreviate; return full or trimmed
    if lower >= text_len:
        if upper >= text_len:
            return text
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # look for a space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    # if no space found
    if index == -1:
        # if upper is at end, return full text
        if upper >= text_len:
            return text
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # if the space is after upper, cut at upper
    if index > upper:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # otherwise cut at the space (exclude the space)
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)