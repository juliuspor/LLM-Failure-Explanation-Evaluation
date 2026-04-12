@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # Normalize upper bound: -1 means no limit
    if upper == -1 or upper > len(text):
        upper = len(text)

    # Reject negative indices
    if lower < 0 or upper < 0:
        raise IndexError(f"String index out of range: {upper}")

    # If lower is beyond text length, nothing to abbreviate — return original
    if lower >= len(text):
        return text

    # Ensure upper is at least lower
    if upper < lower:
        upper = lower

    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        result = substring_java(text, 0, upper)
        if upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)