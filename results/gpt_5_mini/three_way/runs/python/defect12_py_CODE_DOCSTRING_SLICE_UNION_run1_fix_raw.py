@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)

    # Normalize bounds
    if upper == -1 or upper > text_len:
        upper = text_len
    if lower < 0:
        lower = 0
    # If lower is beyond text length, nothing to abbreviate
    if lower >= text_len:
        # No abbreviation possible; return original
        return text
    if upper < lower:
        upper = lower

    # Find space at or after lower
    index = StringUtils.index_of(text, " ", lower)

    # Helper to safely take substring from 0 to end_idx (clamped)
    def safe_substring_end(end_idx: int) -> str:
        if end_idx < 0:
            end_idx = 0
        if end_idx > text_len:
            end_idx = text_len
        return substring_java(text, 0, end_idx)

    if index == -1:
        # No space found after lower
        result = safe_substring_end(upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        return safe_substring_end(upper) + StringUtils.default_string(append_to_end)

    # index is between lower and upper (inclusive), abbreviate at the space
    # ensure index is within bounds
    idx = index
    if idx < 0:
        idx = 0
    if idx > text_len:
        idx = text_len
    return substring_java(text, 0, idx) + StringUtils.default_string(append_to_end)