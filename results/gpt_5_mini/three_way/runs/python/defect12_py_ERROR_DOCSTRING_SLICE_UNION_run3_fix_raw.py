@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # Normalize upper: -1 means no limit -> use full length
    if upper == -1:
        end = len(text)
    else:
        # Clamp upper to text length
        end = min(upper, len(text))

    if end < lower:
        end = lower if lower <= len(text) else len(text)

    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # No space found -> cut at end
        result = substring_java(text, 0, end)
        if end != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > end:
        return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)