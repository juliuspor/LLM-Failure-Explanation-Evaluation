def substring_java(s: str, start: int, end: int) -> str:
    """
    Java-like substring(start, end) with bounds checks.

    Python slicing is safe; Java's String.substring throws if end > length.
    """
    length = len(s)
    # Normalize negative indices (Python behavior)
    if start < 0:
        start += length
    if end < 0:
        end += length
    # Now apply Java-like bounds checks
    if start < 0 or end < 0 or start > end or start > length or end > length:
        raise IndexError(f"String index out of range: {end}")
    return s[start:end]