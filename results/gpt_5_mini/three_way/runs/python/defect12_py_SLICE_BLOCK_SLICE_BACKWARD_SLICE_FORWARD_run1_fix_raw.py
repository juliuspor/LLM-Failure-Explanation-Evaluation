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

    # find a space at or after lower
    index = StringUtils.index_of(text, " ", lower)

    # no space found
    if index == -1:
        # if the text fits within upper, return it unchanged
        if len(text) <= upper:
            return text
        # else cut at upper and append suffix
        result = substring_java(text, 0, upper)
        if upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    # space found after upper -> cut at upper
    if index > upper:
        result = substring_java(text, 0, upper)
        if upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    # space found within bounds: cut at the space
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)