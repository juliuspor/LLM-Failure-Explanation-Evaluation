@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # Normalize upper similar to original behavior: -1 means no limit
    if upper == -1:
        upper = len(text)

    # Clamp bounds into valid range [0, len(text)]
    start_bound = max(0, lower)
    upper_bound = max(0, upper)

    if upper_bound > len(text):
        upper_bound = len(text)

    if upper_bound < start_bound:
        upper_bound = start_bound

    index = StringUtils.index_of(text, " ", start_bound)
    if index == -1:
        result = substring_java(text, 0, upper_bound)
        if upper_bound != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper_bound:
        return substring_java(text, 0, upper_bound) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)