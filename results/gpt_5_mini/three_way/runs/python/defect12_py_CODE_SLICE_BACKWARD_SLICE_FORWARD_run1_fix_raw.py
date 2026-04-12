@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # normalize upper to be within [0, text_len]
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower
    # clamp lower as well
    if lower < 0:
        lower = 0

    # find first space at or after lower
    index = StringUtils.index_of(text, " ", lower)

    # no space found
    if index == -1:
        if upper >= text_len:
            return text
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # space found after upper -> cut at upper
    if index > upper:
        if upper >= text_len:
            return text
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # space found within bounds -> cut at space
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)