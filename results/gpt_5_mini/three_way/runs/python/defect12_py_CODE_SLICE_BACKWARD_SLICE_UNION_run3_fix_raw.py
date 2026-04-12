@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    if upper == -1 or upper > len(text):
        upper = len(text)
    if upper < lower:
        upper = lower

    # Find the first space at or after 'lower'
    index = StringUtils.index_of(text, " ", lower)

    # If no space found or space is after upper, cut at upper
    if index == -1 or index > upper:
        # If upper reaches the end of the text, return full text
        if upper >= len(text):
            return text
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # Space found within bounds: cut at that space
    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)