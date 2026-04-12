@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    """
    Abbreviate `text`, preferably at a word boundary.

    The function looks for a space character at or after `lower`. If a space
    is found before `upper`, the result ends at that space; otherwise the
    result is cut at `upper`. When an abbreviation occurs, `append_to_end`
    (for example `"..."`) is appended.

    Args:
        text: Input string. If None, returns None.
        lower: Minimum index at which to consider abbreviating at a space.
        upper: Maximum end index for the abbreviated string. Use `-1` for no limit.
        append_to_end: Suffix to append when the text is abbreviated.

    Returns:
        The abbreviated string (or None if `text` is None).
    """
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # Safe slicing - Python slicing handles out-of-bounds gracefully
    def safe_substring(start: int, end: int) -> str:
        if start < 0 or end < 0 or start > end:
            raise IndexError(f"String index out of range: {end}")
        return text[min(start, text_len):min(end, text_len)]

    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        result = safe_substring(0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        return safe_substring(0, upper) + StringUtils.default_string(append_to_end)

    return safe_substring(0, index) + StringUtils.default_string(append_to_end)