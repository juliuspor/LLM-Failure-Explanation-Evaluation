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

    # find space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # no space found after lower: cut at upper
        result = substring_java(text, 0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # if found space beyond upper, cut at upper
    if index > upper:
        result = substring_java(text, 0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # cut at the space position
    result = substring_java(text, 0, index)
    if index != text_len:
        result += StringUtils.default_string(append_to_end)
    return result