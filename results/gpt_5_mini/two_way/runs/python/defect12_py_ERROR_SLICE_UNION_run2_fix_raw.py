@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # find the first space at or after 'lower'
    index = StringUtils.index_of(text, " ", lower)
    # if there's no space or the found space is beyond upper, cut at upper
    if index == -1 or index > upper:
        # If we're not cutting the whole text, append the suffix
        result = text[0:upper]
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # otherwise cut at the space
    result = text[0:index]
    result += StringUtils.default_string(append_to_end)
    return result