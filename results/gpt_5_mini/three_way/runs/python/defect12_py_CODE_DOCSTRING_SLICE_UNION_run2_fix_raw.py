@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # Normalize upper: -1 means no limit -> set to len(text)
    if upper == -1 or upper > len(text):
        upper = len(text)
    if upper < lower:
        upper = lower

    # Ensure upper is within bounds [0, len(text)]
    if upper < 0:
        upper = 0
    if upper > len(text):
        upper = len(text)

    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        end = upper if upper <= len(text) else len(text)
        result = substring_java(text, 0, end)
        if end != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        end = upper if upper <= len(text) else len(text)
        return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)