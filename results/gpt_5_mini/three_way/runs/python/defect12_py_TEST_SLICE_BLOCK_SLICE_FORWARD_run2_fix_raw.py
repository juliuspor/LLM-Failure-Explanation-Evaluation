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
        # use Java-like substring with relaxed bounds: clamp to length
        start = 0
        end = upper
        if start < 0 or end < 0 or start > end:
            raise IndexError(f"String index out of range: {end}")
        # clamp
        if start > len(text):
            start = len(text)
        if end > len(text):
            end = len(text)
        result = substring_java(text, start, end)
        if end != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        # clamp as above
        start = 0
        end = upper
        if start < 0 or end < 0 or start > end:
            raise IndexError(f"String index out of range: {end}")
        if start > len(text):
            start = len(text)
        if end > len(text):
            end = len(text)
        return substring_java(text, start, end) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)