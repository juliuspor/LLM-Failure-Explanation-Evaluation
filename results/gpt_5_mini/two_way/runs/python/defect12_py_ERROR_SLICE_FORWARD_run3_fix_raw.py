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

    # find first space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # no space found: cut at upper
        start = 0
        end = upper
        # clamp indices
        if start < 0:
            start = 0
        if end > text_len:
            end = text_len
        if start > end:
            return StringUtils.EMPTY
        result = substring_java(text, start, end)
        if end != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # space found
    if index > upper:
        start = 0
        end = upper
        if start < 0:
            start = 0
        if end > text_len:
            end = text_len
        if start > end:
            return StringUtils.EMPTY
        result = substring_java(text, start, end) + StringUtils.default_string(append_to_end)
        return result

    # truncate at space index
    start = 0
    end = index
    if start < 0:
        start = 0
    if end > text_len:
        end = text_len
    if start > end:
        return StringUtils.EMPTY
    return substring_java(text, start, end) + StringUtils.default_string(append_to_end)