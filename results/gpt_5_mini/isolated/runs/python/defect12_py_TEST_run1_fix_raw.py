@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # normalize bounds
    if lower < 0:
        lower = 0
    if upper == -1:
        upper = len(text)
    if upper > len(text):
        upper = len(text)
    if upper < lower:
        upper = lower

    # if lower is beyond text length, return original
    if lower >= len(text):
        return text

    # find space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # no space found; cut at upper
        result = substring_java(text, 0, upper)
        if upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)