def char_at(s: str, index: int) -> str:
    if not isinstance(index, int):
        raise TypeError(f"index must be int, not {type(index).__name__}")
    if index < 0 or index >= len(s):
        raise IndexError(f"String index out of range: {index}")
    return s[index]