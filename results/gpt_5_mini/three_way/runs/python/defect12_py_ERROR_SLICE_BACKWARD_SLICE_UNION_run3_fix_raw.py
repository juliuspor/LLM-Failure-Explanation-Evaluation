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
    index = text.find(" ", lower)
    if index == -1:
        # No space found after lower; cut at upper
        result = substring_java(text, 0, upper)
        if upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    # If the found space is within upper, use it
    if index <= upper:
        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)

    # Found a space after upper; try to find last space between lower and upper
    last_space = text.rfind(" ", lower, upper + 1)
    if last_space != -1 and last_space >= lower:
        return substring_java(text, 0, last_space) + StringUtils.default_string(append_to_end)

    # No suitable space, cut at upper
    return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)
