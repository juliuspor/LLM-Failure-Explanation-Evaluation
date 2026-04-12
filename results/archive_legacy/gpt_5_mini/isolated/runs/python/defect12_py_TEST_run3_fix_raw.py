@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY
    length = len(text)
    if lower >= length:
        return text
    if upper < 0:
        effective_upper = length
    else:
        effective_upper = upper if upper <= length else length
    if effective_upper < lower:
        effective_upper = lower
    if lower <= 0 and effective_upper >= length:
        return text
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        if effective_upper >= length:
            return text
        return substring_java(text, 0, effective_upper) + StringUtils.default_string(append_to_end)
    if index > effective_upper:
        return substring_java(text, 0, effective_upper) + StringUtils.default_string(append_to_end)
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)