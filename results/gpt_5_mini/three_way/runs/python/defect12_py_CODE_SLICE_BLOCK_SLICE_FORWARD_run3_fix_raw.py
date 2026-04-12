@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # normalize upper: -1 means no limit
    if upper == -1 or upper > text_len:
        upper = text_len
    # ensure lower is within [0, text_len]
    if lower < 0:
        lower = 0
    if lower > text_len:
        lower = text_len
    # ensure upper >= lower
    if upper < lower:
        upper = lower if lower <= text_len else text_len

    # find space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    # if no space or space beyond upper, cut at upper
    if index == -1 or index > upper:
        # substring_java expects end <= len(text)
        end = upper if upper <= text_len else text_len
        result = substring_java(text, 0, end)
        if end != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # space found within bounds: abbreviate at that space
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)