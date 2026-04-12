@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # Treat -1 as no limit
    if upper == -1 or upper > len(text):
        upper = len(text)
    if upper < lower:
        upper = lower

    # Ensure bounds for substring_java: indices must be within [0, len(text)]
    # Find first space at or after 'lower'
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # No space found; cut at upper
        end = upper
        if end > len(text):
            end = len(text)
        result = substring_java(text, 0, end)
        if end != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        end = upper
        if end > len(text):
            end = len(text)
        return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)