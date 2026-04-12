@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    start = lower
    end = upper
    if end == -1:
        end = len(text)
    if start >= len(text):
        return text
    if start < 0 or end < 0 or start > end or end > len(text):
        raise IndexError(f"String index out of range: {end}")

    index = StringUtils.index_of(text, " ", start)
    if index == -1:
        result = substring_java(text, 0, end)
        if end != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > end:
        return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)