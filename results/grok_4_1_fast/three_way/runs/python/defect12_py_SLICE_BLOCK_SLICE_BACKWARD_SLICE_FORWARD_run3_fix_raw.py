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

    n = len(text)
    if upper == -1:
        upper = n
    if upper < lower:
        upper = lower

    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        result = text[:upper]
        if upper != n:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        return text[:upper] + StringUtils.default_string(append_to_end)

    return text[:index] + StringUtils.default_string(append_to_end)

def substring_java(s: str, start: int, end: int) -> str:
    """
    Java-like substring(start, end) with bounds checks.

    Python slicing is safe; Java's String.substring throws if end > length.
    """
    n = len(s)
    # Normalize to Python slicing bounds [0, n]
    start = max(0, min(n, start))
    end = max(0, min(n, end))
    # Handle negative indices (Python style)
    if start < 0:
        start += n
        start = max(0, min(n, start))
    if end < 0:
        end += n
        end = max(0, min(n, end))
    return s[start:end]