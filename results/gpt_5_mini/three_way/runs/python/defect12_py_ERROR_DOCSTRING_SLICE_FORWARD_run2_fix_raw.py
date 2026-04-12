@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)

    # normalize upper: -1 means no limit -> set to text length
    if upper == -1 or upper > text_len:
        upper = text_len
    # ensure upper is at least lower
    if upper < lower:
        upper = lower

    # if lower is beyond text length, nothing to abbreviate
    if lower >= text_len:
        return text

    # find first space at or after lower
    index = StringUtils.index_of(text, " ", lower)

    # if no space found or found beyond upper, cut at upper
    if index == -1 or index > upper:
        # ensure we do not slice beyond text_len
        end = upper if upper <= text_len else text_len
        result = substring_java(text, 0, end)
        if end != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # space found within bounds: abbreviate up to that space
    # ensure index is within bounds
    end = index if index <= text_len else text_len
    result = substring_java(text, 0, end)
    # only append suffix if we actually abbreviated (i.e., end != full length)
    if end != text_len:
        result += StringUtils.default_string(append_to_end)
    return result