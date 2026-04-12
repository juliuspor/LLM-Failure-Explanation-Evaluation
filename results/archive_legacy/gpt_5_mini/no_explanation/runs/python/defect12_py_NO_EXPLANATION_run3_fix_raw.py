@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    if lower < 0:
        lower = 0

    text_len = len(text)
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # If lower is at or beyond text length, just return text (possibly truncated)
    if lower >= text_len:
        # nothing to abbreviate beyond text; return original or truncated
        if upper < text_len:
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)
        return text

    # Look for a space at or after `lower` but before or at `upper`.
    index = text.find(' ', lower)
    if index == -1 or index > upper:
        # No space found in range -> cut at upper
        if upper < text_len:
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)
        return substring_java(text, 0, upper)

    # Found space within [lower, upper]
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)
