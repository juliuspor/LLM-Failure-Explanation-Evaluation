@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)

    if upper == -1:
        upper = text_len
    # If upper exceeds length, clamp it
    if upper > text_len:
        upper = text_len
    # If lower is beyond the end, nothing to abbreviate; return original
    if lower >= text_len:
        return text
    if upper < lower:
        upper = lower

    # Look for a space at or after 'lower' but before or at 'upper'
    # Use find with bounds to avoid indexing beyond length
    index = text.find(" ", lower, upper + 1)
    if index == -1:
        # No space found in the range; cut at upper
        result = substring_java(text, 0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # Found a space within bounds
    if index > upper:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)