@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return ""

    # normalize upper similar to Java logic: -1 means no limit
    if upper == -1 or upper > len(text):
        upper = len(text)
    if upper < lower:
        upper = lower

    # find space at or after `lower`
    index = text.find(" ", lower)
    if index == -1:
        result = substring_java(text, 0, upper)
        if upper != len(text):
            result += (append_to_end or "")
        return result

    if index > upper:
        return substring_java(text, 0, upper) + (append_to_end or "")

    return substring_java(text, 0, index) + (append_to_end or "")