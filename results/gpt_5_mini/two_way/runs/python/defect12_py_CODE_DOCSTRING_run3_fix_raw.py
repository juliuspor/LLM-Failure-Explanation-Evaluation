@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return ""

    # Normalize upper: -1 means no limit
    text_len = len(text)
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # Find first space at or after lower
    index = text.find(" ", lower)
    append_str = "" if append_to_end is None else append_to_end

    if index == -1:
        # No space found; cut at upper
        result = text[0:upper]
        if upper != text_len:
            result += append_str
        return result

    if index > upper:
        # Next space is beyond upper bound; cut at upper
        return text[0:upper] + append_str

    # Space found within bounds; cut at space location
    return text[0:index] + append_str