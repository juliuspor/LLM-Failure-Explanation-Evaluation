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

    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # No space found after lower: if upper reaches the end, return full text
        if upper >= len(text):
            return text
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    if index > upper:
        # Next space is beyond upper: cut at upper
        if upper >= len(text):
            return text
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # Found a space within bounds: cut at the space
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)