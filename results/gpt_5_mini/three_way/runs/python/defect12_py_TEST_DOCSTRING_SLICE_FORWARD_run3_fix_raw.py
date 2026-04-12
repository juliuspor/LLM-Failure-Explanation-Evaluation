@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)

    # normalize lower
    if lower < 0:
        lower = 0
    # if lower beyond text, return original
    if lower >= text_len:
        return text

    # normalize upper: -1 means no limit
    if upper == -1 or upper is None:
        upper = text_len
    if upper < 0:
        upper = 0
    # clamp upper to text length
    if upper > text_len:
        upper = text_len

    # ensure upper >= lower
    if upper < lower:
        upper = lower

    # look for space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    if index == -1 or index > upper:
        # no space found in range -> cut at upper
        end = upper
        # if no abbreviation actually needed, return original
        if end >= text_len:
            return text
        return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

    # space found within range
    # if index is at end of text, nothing to abbreviate
    if index >= text_len:
        return text
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)