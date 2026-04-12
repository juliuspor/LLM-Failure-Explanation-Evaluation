@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    text_len = len(text)
    # normalize upper: -1 means no limit
    if upper == -1 or upper > text_len:
        upper = text_len
    if upper < lower:
        upper = lower

    # if lower is beyond text length, nothing to abbreviate
    if lower >= text_len:
        return text

    # Look for a space at or after 'lower' but no later than 'upper'
    # Python str.find supports an end parameter: search in [lower, upper]
    index = text.find(' ', lower, upper + 1)

    # If no space found in range, we may still need to check if there's any space after lower
    # but before end of text only if upper < text_len and wrap isn't possible — as per logic,
    # when no space within bounds, we cut at upper.
    if index == -1:
        # If upper equals text length, nothing to abbreviate
        if upper >= text_len:
            return text
        # slice up to upper and append suffix
        return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

    # If a space was found at or before upper, cut at the space
    # If the space is at position 0, return empty plus suffix
    if index == 0:
        return StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)