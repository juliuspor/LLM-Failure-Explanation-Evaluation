@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # Normalize upper: -1 means no limit
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # If text is shorter than or equal to upper, nothing to abbreviate
    if text_len <= upper:
        return text

    # If lower is beyond text length, we just truncate at upper and append
    if lower >= text_len:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # Find first space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    # If no space found or space is beyond upper, truncate at upper
    if index == -1 or index > upper:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # Otherwise, abbreviate at the space
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)