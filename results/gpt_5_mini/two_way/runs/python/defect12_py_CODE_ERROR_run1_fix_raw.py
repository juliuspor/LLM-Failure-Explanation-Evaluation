@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # normalize upper: -1 means no limit -> set to text length
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # find first space at or after lower
    index = StringUtils.index_of(text, " ", lower)

    # helper to safe substring up to end (exclusive) ensuring end is within bounds
    def safe_substring(end: int) -> str:
        end_clamped = max(0, min(end, text_len))
        return substring_java(text, 0, end_clamped)

    if index == -1:
        # no space found: cut at upper
        result = safe_substring(upper)
        if upper < text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        result = safe_substring(upper)
        if upper < text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # index is within [lower, upper]
    end = max(0, min(index, text_len))
    result = substring_java(text, 0, end) + StringUtils.default_string(append_to_end)
    return result