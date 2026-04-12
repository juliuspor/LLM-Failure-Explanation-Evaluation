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
    if index == -1:
        start, stop = slice(0, upper).indices(len(text))
        result = text[start:stop]
        if stop != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        start, stop = slice(0, upper).indices(len(text))
        return text[start:stop] + StringUtils.default_string(append_to_end)

    start, stop = slice(0, index).indices(len(text))
    return text[start:stop] + StringUtils.default_string(append_to_end)