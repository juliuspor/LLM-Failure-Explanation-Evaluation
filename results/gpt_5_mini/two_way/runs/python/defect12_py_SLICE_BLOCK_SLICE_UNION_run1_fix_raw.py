@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # Normalize upper similar to Java behavior: -1 means no limit
    if upper == -1 or upper > len(text):
        upper = len(text)
    if upper < lower:
        upper = lower

    # Find first space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # No space found; cut at upper
        result = substring_java(text, 0, upper)
        if upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        # Space occurs beyond upper bound, cut at upper
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # Abbreviate at the space position
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)