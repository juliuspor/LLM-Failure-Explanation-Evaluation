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

    # Look for a space between lower (inclusive) and upper (exclusive)
    index = text.find(" ", lower, upper)
    if index == -1:
        # No space found in the range; if the text is longer than upper, cut at upper and append
        if upper < len(text):
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)
        return substring_java(text, 0, upper)

    # Found a space within bounds; abbreviate at that space
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)