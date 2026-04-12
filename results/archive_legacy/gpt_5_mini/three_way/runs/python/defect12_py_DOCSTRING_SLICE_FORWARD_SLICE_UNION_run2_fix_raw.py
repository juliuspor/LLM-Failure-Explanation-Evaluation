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
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        start = min(max(0, 0), text_len)
        end = min(max(0, upper), text_len)
        result = text[start:end]
        if end != text_len:
            result += StringUtils.default_string(append_to_end)
        return result
    if index > upper:
        start = min(max(0, 0), text_len)
        end = min(max(0, upper), text_len)
        return text[start:end] + StringUtils.default_string(append_to_end)
    start = min(max(0, 0), text_len)
    end = min(max(0, index), text_len)
    return text[start:end] + StringUtils.default_string(append_to_end)
