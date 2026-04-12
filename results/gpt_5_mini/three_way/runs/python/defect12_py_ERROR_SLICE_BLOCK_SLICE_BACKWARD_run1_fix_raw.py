@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # Treat `upper` as an inclusive index per diagnosis. Cap to last valid index.
    if upper == -1 or upper >= len(text):
        upper = len(text) - 1
    if upper < lower:
        upper = lower

    # Find first space at or after `lower`.
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # substring_java expects exclusive end, so use upper+1
        result = substring_java(text, 0, upper + 1)
        if upper != len(text) - 1:
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        return substring_java(text, 0, upper + 1) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)