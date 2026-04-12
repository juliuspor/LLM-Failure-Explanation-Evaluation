def char_at(s: str, index: int) -> str:
    """
    Java-like String.charAt with bounds checks and a Java-style error message.
    """
    if index < 0:
        raise IndexError(f"String index out of range: {index}")
    if index >= len(s):
        raise IndexError(f"String index out of range: {index}")
    return s[index]