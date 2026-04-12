def substring_java(s: str, start: int, end: int) -> str:
    """
    Java-like substring(start, end) with bounds checks.

    Python slicing is safe; Java's String.substring throws if end > length.
    """
    if start < 0 or end < 0 or start > end:
        raise IndexError(f"String index out of range: start={start}, end={end}")
    if start > len(s):
        raise IndexError(f"String index out of range: start={start}")
    return s[start:end]