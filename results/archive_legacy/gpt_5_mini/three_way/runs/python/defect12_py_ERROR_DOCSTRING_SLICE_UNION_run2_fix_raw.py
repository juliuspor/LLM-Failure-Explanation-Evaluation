@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY
    if upper == -1 or upper > len(text):
        effective_upper = len(text)
    else:
        effective_upper = upper
    if effective_upper < lower:
        effective_upper = lower
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        result = text[:effective_upper]
        if effective_upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result
    if index > effective_upper:
        return text[:effective_upper] + StringUtils.default_string(append_to_end)
    return text[:index] + StringUtils.default_string(append_to_end)