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

    # ensure bounds for substring_java: start and end must be within [0, len]
    # we only call substring_java with start=0, so ensure end is between 0 and len
    end_limit = max(0, min(upper, text_len))

    index = StringUtils.index_of(text, " ", max(0, lower))
    if index == -1:
        result = substring_java(text, 0, end_limit)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        return substring_java(text, 0, end_limit) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)