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

    # find first space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # no space found; cut at upper
        end = upper
        result = substring_java(text, 0, end)
        if end != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    # space found
    if index > upper:
        # space beyond upper; cut at upper
        end = upper
        result = substring_java(text, 0, end) + StringUtils.default_string(append_to_end)
        return result

    # space within bounds; cut at the space
    end = index
    return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)