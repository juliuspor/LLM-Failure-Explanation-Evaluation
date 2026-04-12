@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    if upper == -1 or upper > len(text):
        upper = len(text)
    if upper < lower:
        upper = lower

    # Find first space at or after lower
    space_after_lower = StringUtils.index_of(text, " ", lower)
    if space_after_lower == -1:
        # No space after lower: cut at upper
        result = substring_java(text, 0, upper)
        if upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    # If the first space after lower is within upper, cut there
    if space_after_lower <= upper:
        return substring_java(text, 0, space_after_lower) + StringUtils.default_string(append_to_end)

    # Otherwise, look for the last space before or at upper to avoid splitting words earlier
    space_before_upper = text.rfind(" ", 0, upper + 1)
    if space_before_upper >= lower:
        return substring_java(text, 0, space_before_upper) + StringUtils.default_string(append_to_end)

    # Fallback: cut at upper
    return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)