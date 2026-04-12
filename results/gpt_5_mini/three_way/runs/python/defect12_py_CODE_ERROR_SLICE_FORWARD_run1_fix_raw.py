@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # normalize upper to be within bounds
    if upper == -1 or upper > len(text):
        upper = len(text)
    if upper < lower:
        upper = lower

    index = StringUtils.index_of(text, " ", lower)
    # clamp index to text length when non-negative
    if index >= 0 and index > len(text):
        index = len(text)

    if index == -1:
        result = substring_java(text, 0, upper)
        if upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # ensure index does not exceed length
    if index > len(text):
        index = len(text)
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)