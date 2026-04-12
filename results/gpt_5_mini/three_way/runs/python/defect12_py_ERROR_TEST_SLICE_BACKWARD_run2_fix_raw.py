@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # Normalize bounds: lower can be negative -> treat as 0; upper == -1 means no limit
    safe_lower = 0 if lower < 0 else lower
    safe_upper = text_len if upper == -1 else upper
    if safe_upper > text_len:
        safe_upper = text_len
    if safe_upper < safe_lower:
        safe_upper = safe_lower

    index = StringUtils.index_of(text, " ", safe_lower)
    if index == -1:
        # No space found at/after safe_lower: cut at safe_upper
        result = substring_java(text, 0, safe_upper)
        if safe_upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > safe_upper:
        return substring_java(text, 0, safe_upper) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)