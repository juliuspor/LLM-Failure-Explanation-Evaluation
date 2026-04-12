@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    if upper == -1:
        upper = len(text)
    if upper < lower:
        upper = lower

    # Find first space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    if index == -1 or index > upper:
        # No suitable space found, truncate at upper
        result = substring_java(text, 0, upper)
        if upper < len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    # Found space within bounds, truncate there
    result = substring_java(text, 0, index)
    if index < len(text):
        result += StringUtils.default_string(append_to_end)
    return result