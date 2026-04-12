@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return ""

    # normalize bounds
    if lower < 0:
        lower = 0
    text_len = len(text)
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # if lower is beyond text, nothing to abbreviate — return text or maybe append
    if lower >= text_len:
        return text if upper == text_len else (text[:upper] + (append_to_end or ""))

    # find space at or after lower
    try:
        index = text.index(" ", lower)
    except ValueError:
        index = -1

    if index == -1:
        result = text[:upper]
        if upper != text_len:
            result += (append_to_end or "")
        return result

    if index > upper:
        return text[:upper] + (append_to_end or "")

    return text[:index] + (append_to_end or "")