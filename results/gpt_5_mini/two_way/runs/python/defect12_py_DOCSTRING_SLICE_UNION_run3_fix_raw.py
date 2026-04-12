@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # Interpret upper == -1 as no limit
    if upper == -1 or upper > text_len:
        upper_clamped = text_len
    else:
        upper_clamped = upper

    if upper_clamped < lower:
        upper_clamped = lower

    # Find first space at or after 'lower'
    index = StringUtils.index_of(text, " ", lower)

    # No space found after 'lower'
    if index == -1:
        end = upper_clamped
        # ensure end is within bounds
        if end < 0:
            end = 0
        result = substring_java(text, 0, end)
        if end != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # Space found; if it lies beyond the allowed upper bound, cut at upper
    if index > upper_clamped:
        end = upper_clamped
        if end < 0:
            end = 0
        return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

    # Otherwise abbreviate at the space
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)