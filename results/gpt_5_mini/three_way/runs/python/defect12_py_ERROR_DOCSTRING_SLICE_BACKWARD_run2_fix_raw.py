@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # Treat -1 as no limit (use full length)
    if upper == -1:
        upper = text_len
    # Clamp upper to the string length
    if upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # No space found after lower: cut at upper
        result = substring_java(text, 0, min(upper, text_len))
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        return substring_java(text, 0, min(upper, text_len)) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)