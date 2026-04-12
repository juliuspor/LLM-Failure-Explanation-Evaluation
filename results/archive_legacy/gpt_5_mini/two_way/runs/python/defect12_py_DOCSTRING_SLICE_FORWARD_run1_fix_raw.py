@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY
    length = len(text)
    if upper == -1 or upper > length:
        upper = length
    if upper < lower:
        upper = lower
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        end = max(0, min(upper, length))
        result = text[0:end]
        if end != length:
            result += StringUtils.default_string(append_to_end)
        return result
    if index > upper:
        end = max(0, min(upper, length))
        return text[0:end] + StringUtils.default_string(append_to_end)
    idx = max(0, min(index, length))
    return text[0:idx] + StringUtils.default_string(append_to_end)