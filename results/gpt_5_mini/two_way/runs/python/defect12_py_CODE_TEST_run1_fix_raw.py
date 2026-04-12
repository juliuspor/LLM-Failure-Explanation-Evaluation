@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return ""

    text_len = len(text)
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # If lower is beyond text length, nothing to abbreviate; return original
    if lower >= text_len:
        return text

    # Find first space at or after lower
    index = text.find(" ", lower)
    append = "" if append_to_end is None else append_to_end

    if index == -1:
        # No space found; cut at upper
        result = text[0:upper]
        if upper != text_len:
            result += append
        return result

    if index > upper:
        res = text[0:upper]
        if upper != text_len:
            res += append
        return res

    # index is within [lower, upper]
    res = text[0:index]
    if index != text_len:
        res += append
    return res