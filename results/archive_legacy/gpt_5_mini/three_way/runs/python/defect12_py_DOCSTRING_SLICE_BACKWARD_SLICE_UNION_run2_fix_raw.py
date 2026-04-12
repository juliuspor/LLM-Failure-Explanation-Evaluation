@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    if upper == -1 or upper > len(text):
        upper = len(text)
    if upper < lower:
        upper = lower

    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        start = 0
        s_start = min(start, len(text))
        s_end = min(upper, len(text))
        result = substring_java(text, s_start, s_end)
        if upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        s_start = 0
        s_end = min(upper, len(text))
        return substring_java(text, s_start, s_end) + StringUtils.default_string(append_to_end)

    s_start = 0
    s_end = min(index, len(text))
    return substring_java(text, s_start, s_end) + StringUtils.default_string(append_to_end)