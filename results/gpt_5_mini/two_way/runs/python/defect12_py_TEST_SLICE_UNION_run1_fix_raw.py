@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # normalize bounds: treat upper == -1 as no limit
    if upper == -1 or upper > text_len:
        upper = text_len
    if lower < 0:
        lower = 0
    if upper < lower:
        upper = lower

    # if lower beyond text, nothing to abbreviate
    if lower >= text_len:
        return text

    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # clamp end to text length
        end = min(upper, text_len)
        result = substring_java(text, 0, end)
        if end != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        end = min(upper, text_len)
        return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)