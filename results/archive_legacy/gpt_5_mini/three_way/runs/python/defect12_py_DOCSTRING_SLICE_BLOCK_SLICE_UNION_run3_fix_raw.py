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
        end = max(0, min(upper, len(text)))
        result = substring_java(text, 0, end)
        if end != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        end = max(0, min(upper, len(text)))
        return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

    idx = max(0, min(index, len(text)))
    return substring_java(text, 0, idx) + StringUtils.default_string(append_to_end)