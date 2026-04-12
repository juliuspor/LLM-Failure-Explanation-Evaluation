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
    # Normalize upper
    if upper > text_len:
        upper = text_len
    # If upper < lower, normalize to lower (but also cap at text_len)
    if upper < lower:
        upper = min(lower, text_len)

    # If lower is beyond the string, nothing to abbreviate
    if lower >= text_len:
        return text

    # Ensure start index for search is within bounds
    search_start = max(0, min(lower, text_len))
    index = StringUtils.index_of(text, " ", search_start)

    # No space found after lower
    if index == -1:
        # If upper covers the whole string, return original
        if upper >= text_len:
            return text
        # Otherwise cut at upper and append suffix
        result = substring_java(text, 0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # Space found
    if index > upper:
        # space is beyond upper, cut at upper
        result = substring_java(text, 0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # Space within bounds: cut at the space
    result = substring_java(text, 0, index)
    if index != text_len:
        result += StringUtils.default_string(append_to_end)
    return result