@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # Clamp lower and upper to valid ranges [0, text_len]
    if lower < 0:
        lower = 0
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower
    if lower > text_len:
        # lower beyond end: nothing to abbreviate; return original or truncated with append if needed
        if upper >= text_len:
            return text
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # Ensure index_of start is within bounds
    index = StringUtils.index_of(text, " ", lower if lower <= text_len else text_len)
    if index == -1:
        result = substring_java(text, 0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)