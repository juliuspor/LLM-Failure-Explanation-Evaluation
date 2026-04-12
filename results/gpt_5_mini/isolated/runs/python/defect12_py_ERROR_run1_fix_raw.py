@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)

    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    index = StringUtils.index_of(text, " ", lower)
    # If no space found or the found space is beyond the allowed upper bound,
    # cut at upper. Ensure substring_java is called with end <= len(text).
    if index == -1 or index > upper:
        end = upper
        # substring_java requires end <= len(text)
        if end > text_len:
            end = text_len
        result = substring_java(text, 0, end)
        if end != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # Found a space within bounds
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)