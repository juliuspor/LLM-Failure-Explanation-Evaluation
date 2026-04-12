@staticmethod
def abbreviate(text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY
    if lower is None or not isinstance(lower, int):
        try:
            lower = int(lower)
        except Exception:
            raise TypeError("lower must be an int or int-convertible")
    if upper is None or not isinstance(upper, int):
        try:
            upper = int(upper)
        except Exception:
            raise TypeError("upper must be an int or int-convertible")
    if lower < 0:
        lower = 0
    text_len = len(text)
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower
    if lower >= text_len:
        result = substring_java(text, 0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        result = substring_java(text, 0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result
    if index > upper:
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)