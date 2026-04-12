@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # Normalize upper: -1 means no limit
    if upper == -1:
        upper = len(text)

    # Clamp bounds to valid range [0, len(text)]
    start = max(0, lower)
    end = max(0, upper)
    if start > len(text):
        # start beyond text means no abbreviation needed
        return text
    if end > len(text):
        end = len(text)
    if end < start:
        end = start

    # If there's no space at or after `start`, or start==0 and end covers whole text,
    # follow original behavior: try to find a space at/after lower; if none, cut at end
    index = StringUtils.index_of(text, " ", start)
    if index == -1:
        result = substring_java(text, 0, end)
        if end != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > end:
        return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

    return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)