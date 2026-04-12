@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY
    if upper == -1 or upper > len(text):
        upper = len(text)
    if upper < lower:
        upper = lower
    index = StringUtils.index_of(text, " ", lower)
    def clamp_slice(s: str, start: int, end: int) -> str:
        start = max(0, min(start, len(s)))
        end = max(0, min(end, len(s)))
        return s[start:end]
    if index == -1:
        result = clamp_slice(text, 0, upper)
        if upper != len(text):
            result += StringUtils.default_string(append_to_end)
        return result
    if index > upper:
        return clamp_slice(text, 0, upper) + StringUtils.default_string(append_to_end)
    return clamp_slice(text, 0, index) + StringUtils.default_string(append_to_end)