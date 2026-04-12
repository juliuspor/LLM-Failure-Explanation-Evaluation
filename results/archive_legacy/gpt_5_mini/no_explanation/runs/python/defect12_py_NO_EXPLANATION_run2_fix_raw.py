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
    if lower < 0:
        lower = 0
    if upper < lower:
        upper = lower

    # If the text is already within upper, no abbreviation
    if len(text) <= upper:
        return text

    # Find the first space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    # If no space found or space is beyond upper, cut at upper
    if index == -1 or index > upper:
        result = substring_java(text, 0, upper)
        if upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    # Found a space within bounds; cut at that space
    result = substring_java(text, 0, index)
    result += StringUtils.default_string(append_to_end)
    return result