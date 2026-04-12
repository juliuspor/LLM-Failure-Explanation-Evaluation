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

    # Look for a space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    # If no space found or space is beyond upper, try to find the last space before upper
    if index == -1 or index > upper:
        # Try to find a space between lower and upper (inclusive)
        space_before_upper = text.rfind(" ", lower, upper + 1)
        if space_before_upper != -1 and space_before_upper >= lower:
            return substring_java(text, 0, space_before_upper) + StringUtils.default_string(append_to_end)
        # No suitable space found: cut at upper
        result = substring_java(text, 0, upper)
        if upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    # Found a space within the allowed range
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)