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

    # Find the first space at or after 'lower'
    index = StringUtils.index_of(text, " ", lower)
    # If no space found or the space is beyond the allowed upper bound,
    # cut at upper
    if index == -1 or index > upper:
        # Clamp upper to text length to avoid IndexError
        end = upper if upper <= text_len else text_len
        result = substring_java(text, 0, end)
        if end != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # Found a space within [lower, upper], abbreviate at that space
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)