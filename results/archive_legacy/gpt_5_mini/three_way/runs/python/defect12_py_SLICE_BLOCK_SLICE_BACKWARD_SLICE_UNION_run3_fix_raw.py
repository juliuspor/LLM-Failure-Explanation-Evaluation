@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY
    text_len = len(text)
    if lower is None:
        lower = 0
    if upper is None or upper == -1:
        upper = text_len
    if lower < 0:
        lower += text_len
    if upper < 0:
        upper += text_len
    if upper < lower:
        upper = lower
    if lower < 0 or upper < 0 or lower > text_len or upper > text_len or lower > upper:
        raise IndexError(f"String index out of range: start={lower}, end={upper}")
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        result = substring_java(text, 0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result
    if index > upper:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)