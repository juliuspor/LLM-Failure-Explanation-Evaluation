@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # Normalize upper: -1 means no limit
    if upper == -1 or upper > len(text):
        upper = len(text)
    if upper < lower:
        upper = lower

    # Find a space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    # If no space found or space is beyond upper, cut at upper
    if index == -1 or index > upper:
        result = substring_java(text, 0, upper)
        if upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    # Found a space within bounds -> cut at that space
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)