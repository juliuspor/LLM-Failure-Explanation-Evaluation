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
    if upper < lower:
        upper = lower

    # If lower is at or beyond text length, nothing to abbreviate; return original or append if truncated
    if lower >= text_len:
        return text if upper >= text_len else StringUtils.default_string(append_to_end)

    index = StringUtils.index_of(text, " ", lower)
    # If no space found or space is beyond upper, cut at upper
    if index == -1 or index > upper - 1:
        # slice safely up to upper
        result = substring_java(text, 0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # index is within bounds and <= upper-1, safe to use
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)