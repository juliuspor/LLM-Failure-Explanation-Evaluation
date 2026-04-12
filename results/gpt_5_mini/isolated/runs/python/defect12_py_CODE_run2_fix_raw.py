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

    index = text.find(" ", lower)
    if index == -1:
        # No space found after lower: cut at upper
        result = text[0:upper]
        if upper != text_len:
            result += "" if append_to_end is None else append_to_end
        return result

    if index > upper:
        result = text[0:upper]
        result += "" if append_to_end is None else append_to_end
        return result

    # Found space between lower and upper inclusive
    result = text[0:index]
    result += "" if append_to_end is None else append_to_end
    return result