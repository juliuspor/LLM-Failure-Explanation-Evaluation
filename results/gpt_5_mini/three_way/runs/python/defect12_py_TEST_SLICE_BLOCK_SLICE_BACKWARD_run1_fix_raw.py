@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # Interpret upper == -1 as no limit
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # safe slicing: clamp upper to text length
        end = upper if upper <= text_len else text_len
        result = text[0:end]
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        end = upper if upper <= text_len else text_len
        return text[0:end] + StringUtils.default_string(append_to_end)

    # index is within bounds (could be equal to text_len)
    end = index if index <= text_len else text_len
    return text[0:end] + StringUtils.default_string(append_to_end)