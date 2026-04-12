@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)

    # Clamp bounds
    if lower < 0:
        lower = 0
    if lower > text_len:
        lower = text_len

    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    index = StringUtils.index_of(text, " ", lower)
    # If no space found or space is beyond upper, abbreviate at upper
    if index == -1 or index > upper:
        end = min(upper, text_len)
        result = substring_java(text, 0, end)
        if end != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # Found a space within bounds
    end = min(index, text_len)
    return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)