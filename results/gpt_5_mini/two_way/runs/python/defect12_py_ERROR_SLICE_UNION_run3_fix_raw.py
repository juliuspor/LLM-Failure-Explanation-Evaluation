@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # Ensure upper is within acceptable bounds for this runtime where end must be <= len(text)-1
    if upper == -1:
        upper = len(text) - 1
    elif upper > len(text) - 1:
        upper = len(text) - 1
    if upper < lower:
        upper = lower

    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # take up to upper (inclusive end index in this runtime), so slice to upper+1
        end_index = upper + 1
        result = text[0:end_index]
        if end_index - 1 != len(text) - 1:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        end_index = upper + 1
        return text[0:end_index] + StringUtils.default_string(append_to_end)

    # index is within bounds, take up to index (exclude the space)
    return text[0:index] + StringUtils.default_string(append_to_end)