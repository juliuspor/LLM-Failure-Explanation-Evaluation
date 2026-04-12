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

    # find the first space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    # if no space found or the found space is at/after upper, cut at upper
    if index == -1 or index >= upper:
        result = substring_java(text, 0, upper)
        if upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    # otherwise cut at the space index
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)