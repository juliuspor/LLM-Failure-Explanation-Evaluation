@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # normalize bounds
    if lower < 0:
        lower = 0
    if upper == -1:
        upper = len(text)
    if upper > len(text):
        upper = len(text)
    if upper < lower:
        upper = lower

    # search for a space at or after 'lower' but not beyond 'upper'
    # prefer to break at a space index if within bounds
    index = text.find(' ', lower)
    if index == -1 or index > upper:
        # no space found in range -> cut at upper
        end = upper
    else:
        end = index

    result = text[:end]
    # append suffix only if we actually abbreviated (i.e., trimmed off chars)
    if end < len(text):
        result += StringUtils.default_string(append_to_end)
    return result