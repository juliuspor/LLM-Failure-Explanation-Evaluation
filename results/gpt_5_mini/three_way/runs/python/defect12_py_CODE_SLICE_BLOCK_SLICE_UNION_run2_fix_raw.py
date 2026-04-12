@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # Clamp bounds to valid range
    if lower < 0:
        lower = 0
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # Ensure we don't search starting beyond the string
    search_start = lower if lower <= text_len else text_len
    index = StringUtils.index_of(text, " ", search_start)
    if index == -1:
        end = upper if upper <= text_len else text_len
        result = substring_java(text, 0, end)
        if end != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        end = upper if upper <= text_len else text_len
        return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

    # index is within bounds
    end = index if index <= text_len else text_len
    return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)