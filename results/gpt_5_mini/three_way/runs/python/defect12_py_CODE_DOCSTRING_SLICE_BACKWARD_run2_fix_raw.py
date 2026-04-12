@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # Normalize upper to be within valid bounds (0..len(text))
    text_len = len(text)
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # Find the first space at or after `lower`
    index = StringUtils.index_of(text, " ", lower)

    # If no space found, cut at upper
    if index == -1:
        # Ensure upper is not beyond text length (already normalized)
        result = substring_java(text, 0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # If the found space is beyond the allowed upper bound, cut at upper
    if index > upper:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # Otherwise cut at the space
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)