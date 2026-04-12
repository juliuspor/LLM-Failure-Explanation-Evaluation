@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # Validate types for lower and upper
    if not isinstance(lower, int) or not isinstance(upper, int):
        raise TypeError(f"lower and upper must be integers: got lower={type(lower).__name__}, upper={type(upper).__name__}")

    text_len = len(text)

    # Normalize upper: -1 means no limit
    if upper == -1:
        upper = text_len

    # Clamp bounds
    if lower < 0:
        lower = 0
    if upper < 0:
        upper = 0
    if upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        result = substring_java(text, 0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)