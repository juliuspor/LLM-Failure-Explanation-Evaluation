@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return ''

    if upper == -1 or upper > len(text):
        upper = len(text)
    if upper < lower:
        upper = lower

    index = text.find(' ', lower)
    if index == -1:
        if upper > len(text):
            raise IndexError(f"String index out of range: {upper}")
        result = text[:upper]
        if upper != len(text):
            result += (append_to_end or '')
        return result

    if index > upper:
        if upper > len(text):
            raise IndexError(f"String index out of range: {upper}")
        return text[:upper] + (append_to_end or '')

    return text[:index] + (append_to_end or '')