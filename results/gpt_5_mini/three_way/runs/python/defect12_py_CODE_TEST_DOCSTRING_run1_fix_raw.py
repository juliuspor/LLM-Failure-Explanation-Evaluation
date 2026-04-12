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
        result = text[0:upper]
        if upper != text_len:
            result += "" if append_to_end is None else append_to_end
        return result

    if index > upper:
        return text[0:upper] + ("" if append_to_end is None else append_to_end)

    return text[0:index] + ("" if append_to_end is None else append_to_end)