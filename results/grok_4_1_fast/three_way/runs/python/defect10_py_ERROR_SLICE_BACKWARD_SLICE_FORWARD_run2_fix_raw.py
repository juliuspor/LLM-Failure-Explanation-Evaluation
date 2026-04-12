def char_at(s: str, index: int) -> str:
    """
    Java-like String.charAt with bounds checks and a Java-style error message.
    """
    try:
        index = int(index)
    except (ValueError, TypeError):
        raise IndexError(f"String index out of range: {index}") from None
    if index < 0 or index >= len(s):
        raise IndexError(f"String index out of range: {index}")
    return s[index]