@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # Normalize upper: -1 means no limit
    if upper == -1:
        upper = text_len
    # Clamp upper within bounds
    if upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # Find the first space at or after lower
    index = StringUtils.index_of(text, " ", lower)

    # Helper to append suffix only when abbreviation actually truncates
    def _with_suffix(end_index: int) -> str:
        result = substring_java(text, 0, end_index)
        if end_index < text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    if index == -1:
        # No space found; cut at upper
        return _with_suffix(upper)

    if index > upper:
        return _with_suffix(upper)

    return _with_suffix(index)