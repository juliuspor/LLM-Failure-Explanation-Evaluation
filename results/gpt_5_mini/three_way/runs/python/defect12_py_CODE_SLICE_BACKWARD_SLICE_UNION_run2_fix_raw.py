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

    # If lower is beyond text length, nothing to abbreviate
    if lower >= text_len:
        # no abbreviation possible; return text (and maybe append if upper < text_len, but here upper==text_len)
        return text

    # Ensure upper is not less than lower
    if upper < lower:
        upper = lower

    # Now safe to search for space at/after lower
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # No space found; cut at upper
        result = substring_java(text, 0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)