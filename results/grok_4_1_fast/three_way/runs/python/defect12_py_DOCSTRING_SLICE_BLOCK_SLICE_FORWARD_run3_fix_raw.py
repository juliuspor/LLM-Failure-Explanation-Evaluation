def substring_java(s: str, start: int, end: int) -> str:
    """
    Java-like substring(start, end) with bounds checks.

    Python slicing is safe; Java's String.substring throws if end > length.
    """
    if start < 0 or end < 0:
        raise IndexError(f"String index out of range: {end}")
    if end == -1:
        end = len(s)
    if start > end or start > len(s) or end > len(s):
        raise IndexError(f"String index out of range: {end}")
    return s[start:end]