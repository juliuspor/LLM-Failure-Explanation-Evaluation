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
        # keep semantics: if upper < lower, set upper to lower but cap to text length
        upper = min(lower, text_len)

    # find space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # no space found after lower; cut at upper
        # ensure end bound is within string
        end = min(upper, text_len)
        result = substring_java(text, 0, end)
        if end < text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        end = min(upper, text_len)
        return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

    # space found within bounds
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)