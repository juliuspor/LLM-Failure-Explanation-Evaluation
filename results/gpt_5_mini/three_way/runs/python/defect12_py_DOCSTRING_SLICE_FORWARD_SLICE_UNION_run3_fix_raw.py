@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # Normalize upper: -1 means no limit; cap to length
    effective_upper = len(text) if upper == -1 else upper
    if effective_upper > len(text):
        effective_upper = len(text)
    if effective_upper < lower:
        effective_upper = lower

    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        result = substring_java(text, 0, effective_upper)
        if effective_upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > effective_upper:
        return substring_java(text, 0, effective_upper) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)