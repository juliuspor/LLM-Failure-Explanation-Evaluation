@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)

    # normalize lower and upper
    if lower < 0:
        lower = 0
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # find first space at or after lower
    index = StringUtils.index_of(text, " ", lower)

    # no space found
    if index == -1:
        # ensure end is within bounds
        end = upper if 0 <= upper <= text_len else text_len
        result = substring_java(text, 0, end)
        if end != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # space found after lower
    if index > upper:
        end = upper if 0 <= upper <= text_len else text_len
        return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

    # truncate at the space
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)