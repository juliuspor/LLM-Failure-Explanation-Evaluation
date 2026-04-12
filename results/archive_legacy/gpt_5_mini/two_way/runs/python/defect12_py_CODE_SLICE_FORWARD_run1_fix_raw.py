@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY
    if not isinstance(lower, int):
        raise TypeError(f"lower must be int, got {type(lower).__name__}")
    if not isinstance(upper, int):
        raise TypeError(f"upper must be int, got {type(upper).__name__}")
    if upper == -1 or upper > len(text):
        upper = len(text)
    if upper < lower:
        upper = lower
    index = StringUtils.index_of(text, " ", lower)
    if not isinstance(index, int):
        raise TypeError(f"index must be int, got {type(index).__name__}")
    if index == -1:
        result = substring_java(text, 0, upper)
        if upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result
    if index > upper:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)