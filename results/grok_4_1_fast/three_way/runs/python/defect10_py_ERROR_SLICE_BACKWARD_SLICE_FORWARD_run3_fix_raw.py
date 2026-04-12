def char_at(s: str, index: int) -> str:
    """
    Java-like String.charAt with bounds checks and a Java-style error message.
    """
    if not isinstance(index, int):
        raise IndexError(f"String index out of range: {index}")
    if index < 0 or index >= len(s):
        raise IndexError(f"String index out of range: {index}")
    return s[index]