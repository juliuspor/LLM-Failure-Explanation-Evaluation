@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY
    if lower < 0 or upper < -1:
        raise IndexError(f"String index out of range: start={lower}, end={upper}")
    if upper == -1 or upper > len(text):
        upper = len(text)
    if upper < lower:
        upper = lower
    if lower > len(text):
        index = -1
    else:
        index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        start = 0
        end = min(upper, len(text))
        result = text[start:end]
        if end != len(text):
            result += StringUtils.default_string(append_to_end)
        return result
    if index > upper:
        start = 0
        end = min(upper, len(text))
        return text[start:end] + StringUtils.default_string(append_to_end)
    return text[0:index] + StringUtils.default_string(append_to_end)