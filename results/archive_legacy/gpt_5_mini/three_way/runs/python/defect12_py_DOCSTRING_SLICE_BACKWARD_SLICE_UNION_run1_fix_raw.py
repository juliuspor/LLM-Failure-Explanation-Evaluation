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
    end = min(upper, len(text))
    if index == -1:
        result = text[0:end]
        if end != len(text):
            result += StringUtils.default_string(append_to_end)
        return result
    if index > upper:
        return text[0:end] + StringUtils.default_string(append_to_end)
    return text[0:min(index, len(text))] + StringUtils.default_string(append_to_end)