@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # Normalize upper (-1 means no limit)
    if upper == -1:
        upper_index = len(text)
    else:
        upper_index = upper if upper is not None else len(text)
    if upper_index > len(text):
        upper_index = len(text)
    if upper_index < lower:
        upper_index = lower

    # Find the first space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # No space found: cut at upper_index
        # If lower (start) is beyond text length, return original text
        if lower >= len(text):
            return text
        start = max(0, 0)
        end = upper_index
        result = text[start:end]
        if end != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper_index:
        # space found after upper_index -> cut at upper_index
        if 0 >= len(text):
            return text
        start = 0
        end = upper_index
        return text[start:end] + StringUtils.default_string(append_to_end)

    # space found within bounds -> cut at the space
    return text[0:index] + StringUtils.default_string(append_to_end)