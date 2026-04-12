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

    # Ensure lower and upper are within bounds
    if lower < 0:
        raise IndexError(f"String index out of range: {lower}")
    if upper < 0:
        raise IndexError(f"String index out of range: {upper}")

    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # cap upper to length to avoid slicing beyond end
        end = min(upper, len(text))
        result = substring_java(text, 0, end)
        if upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        end = min(upper, len(text))
        return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)