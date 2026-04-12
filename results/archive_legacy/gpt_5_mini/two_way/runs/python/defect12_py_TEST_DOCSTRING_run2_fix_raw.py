@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY
    if lower < 0:
        lower = 0
    length = len(text)
    if upper == -1:
        upper = length
    if lower >= length:
        return text
    if upper > length:
        upper = length
    if upper < lower:
        upper = lower
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        result = substring_java(text, 0, upper)
        if upper != length:
            result += StringUtils.default_string(append_to_end)
        return result
    if index > upper:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)