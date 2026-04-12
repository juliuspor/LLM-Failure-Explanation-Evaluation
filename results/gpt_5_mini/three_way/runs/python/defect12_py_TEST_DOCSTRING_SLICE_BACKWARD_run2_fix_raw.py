@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # Interpret upper == -1 as no limit (end of text)
    if upper == -1 or upper > text_len:
        adj_upper = text_len
    else:
        adj_upper = upper
    if adj_upper < lower:
        adj_upper = lower

    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        result = substring_java(text, 0, adj_upper)
        if adj_upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > adj_upper:
        return substring_java(text, 0, adj_upper) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)