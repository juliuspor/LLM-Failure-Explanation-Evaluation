@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # Normalize upper similar to original behavior: -1 means no limit
    if upper == -1 or upper > len(text):
        upper = len(text)
    if upper < lower:
        upper = lower

    # Find first space at or after 'lower'
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # No space found; return up to upper (clamped)
        # If lower >= len(text), return the whole text
        if lower >= len(text):
            return text
        # clamp end to len(text)
        end = min(upper, len(text))
        result = substring_java(text, 0, end)
        if end != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        # Space found after upper; cut at upper
        end = min(upper, len(text))
        return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

    # Space found within bounds; cut at that space
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)