@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY
    text_len = len(text)
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower
    if lower >= text_len:
        return text
    start = max(0, lower)
    index = StringUtils.index_of(text, " ", start)
    if index == -1:
        end = max(0, min(upper, text_len))
        result = text[0:end]
        if end != text_len:
            result += StringUtils.default_string(append_to_end)
        return result
    if index > upper:
        end = max(0, min(upper, text_len))
        return text[0:end] + StringUtils.default_string(append_to_end)
    return text[0:index] + StringUtils.default_string(append_to_end)