@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY
    if lower >= len(text):
        return text
    upper_limit = None
    if upper == -1:
        upper_limit = None
    else:
        if upper > len(text):
            upper = len(text)
        if upper < lower:
            upper = lower
        upper_limit = upper
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        if upper_limit is None:
            return text
        result = substring_java(text, 0, upper_limit)
        if upper_limit != len(text):
            result += StringUtils.default_string(append_to_end)
        return result
    if upper_limit is None:
        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)
    if index > upper_limit:
        return substring_java(text, 0, upper_limit) + StringUtils.default_string(append_to_end)
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)