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

    # Find first space at or after lower
    index = StringUtils.index_of(text, " ", lower)

    # No space found
    if index == -1:
        # take up to upper (which is at most len(text))
        result = substring_java(text, 0, upper)
        if upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    # Space found after upper -> cut at upper
    if index > upper:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # Space found within bounds -> cut at that space
    # Ensure index is within bounds [0, len(text)] before slicing
    end = index if index <= len(text) else len(text)
    return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)