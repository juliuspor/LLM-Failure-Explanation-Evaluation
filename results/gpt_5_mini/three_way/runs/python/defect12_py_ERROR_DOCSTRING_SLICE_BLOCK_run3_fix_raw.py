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
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # Find first space at or after 'lower'
    index = StringUtils.index_of(text, " ", lower)

    # If no space found, or space is beyond upper, cut at upper
    if index == -1 or index > upper:
        result = substring_java(text, 0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # Space found within bounds: cut at the space
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)