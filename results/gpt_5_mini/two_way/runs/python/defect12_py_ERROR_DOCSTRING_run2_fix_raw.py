@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    n = len(text)
    # handle upper == -1 as no limit
    if upper == -1 or upper > n:
        upper = n
    if upper < lower:
        upper = lower

    # If lower is beyond the end of the string, there's no space to find
    if lower >= n:
        # nothing to search; just truncate to upper
        result = substring_java(text, 0, upper)
        if upper != n:
            result += StringUtils.default_string(append_to_end)
        return result

    # find a space at or after lower
    index = text.find(' ', lower)
    if index == -1:
        result = substring_java(text, 0, upper)
        if upper != n:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)