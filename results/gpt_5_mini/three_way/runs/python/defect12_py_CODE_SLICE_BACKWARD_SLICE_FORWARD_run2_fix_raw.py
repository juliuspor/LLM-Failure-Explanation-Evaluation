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

    index = StringUtils.index_of(text, " ", lower)
    # normalize index to be within [-1, text_len]
    if index < -1:
        index = -1
    if index > text_len:
        index = text_len

    def bounded_substring(end: int) -> str:
        if end < 0:
            end = 0
        if end > text_len:
            end = text_len
        return substring_java(text, 0, end)

    if index == -1:
        result = bounded_substring(upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        return bounded_substring(upper) + StringUtils.default_string(append_to_end)

    return bounded_substring(index) + StringUtils.default_string(append_to_end)