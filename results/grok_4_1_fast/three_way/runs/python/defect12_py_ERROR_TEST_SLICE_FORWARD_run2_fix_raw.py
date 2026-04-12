@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    if upper == -1:
        upper = text_len
    if upper > text_len:
        upper = text_len
    if lower < 0:
        lower = 0
    elif lower > text_len:
        lower = text_len
    
    if lower >= upper:
        return text

    index = StringUtils.index_of(text, " ", lower)
    if index == -1 or index > upper:
        result = substring_java(text, 0, upper)
        if upper < text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)

def substring_java(s: str, start: int, end: int) -> str:
    """
    Java-like substring(start, end) with bounds checks.

    Python slicing is safe; Java's String.substring throws if end > length.
    """
    if start < 0:
        start = 0
    if end < 0:
        end = 0
    if start > end:
        end = start
    if end > len(s):
        end = len(s)
    if start > len(s):
        raise IndexError(f"String index out of range: {start}")
    return s[start:end]