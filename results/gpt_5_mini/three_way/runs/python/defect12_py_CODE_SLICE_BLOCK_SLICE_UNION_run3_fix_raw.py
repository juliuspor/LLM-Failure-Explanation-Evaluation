@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)

    # clamp lower to valid range
    if lower < 0:
        lower = 0
    if lower > text_len:
        lower = text_len

    # normalize upper: -1 means no limit; clamp to text length
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    index = StringUtils.index_of(text, " ", lower)

    # normalize index: if not found or out of range, treat as end of string
    if index == -1 or index > text_len:
        index = text_len

    if index == text_len:
        # no space found after lower within the string
        end = min(upper, text_len)
        result = substring_java(text, 0, end)
        if end != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # found a space at or after lower
    if index > upper:
        end = min(upper, text_len)
        return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

    # index is within bounds and <= upper
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)