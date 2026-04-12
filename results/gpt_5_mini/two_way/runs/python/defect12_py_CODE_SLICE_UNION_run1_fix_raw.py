@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # normalize upper
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # If lower is beyond text length, nothing to abbreviate; return text as is
    if lower >= text_len:
        return text

    index = StringUtils.index_of(text, " ", lower)

    # no space found at/after lower
    if index == -1:
        # if upper covers entire text, return original
        if upper >= text_len:
            return text
        # otherwise return truncated + append
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # found a space
    if index > upper:
        if upper >= text_len:
            return text
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # index is within upper bound: cut at the space
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)