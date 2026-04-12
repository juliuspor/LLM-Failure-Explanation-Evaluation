def substring_java(s: str, start: int, end: int) -> str:
    """
    Java-like substring(start, end) with bounds checking.
    """
    if start < 0 or end < 0 or start > end or start >= len(s) or end > len(s):
        raise IndexError(f"String index out of range: {end}")
    return s[start:end]