@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    effective_upper = len(text) if upper == -1 else min(upper, len(text))
    if effective_upper < lower:
        effective_upper = lower

    index = StringUtils.index_of(text, " ", lower, effective_upper)
    if index == -1 or index > effective_upper:
        result = substring_java(text, 0, effective_upper)
        if effective_upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)