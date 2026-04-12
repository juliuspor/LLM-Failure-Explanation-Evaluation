@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # Validate types
    if not isinstance(lower, int) or (upper != -1 and not isinstance(upper, int)):
        raise ValueError("lower and upper must be integers (upper may be -1)")

    if upper == -1 or upper > len(text):
        upper = len(text)
    if upper < lower:
        upper = lower

    # Find space at or after lower
    index = StringUtils.index_of(text, " ", lower)
    if index == -1:
        # No space found: cut at upper
        start = 0
        end = upper
        # Clamp indices
        start = max(0, start)
        end = min(len(text), end)
        # Ensure ints
        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError("Computed slice indices must be integers")
        result = substring_java(text, start, end)
        if end != len(text):
            result += StringUtils.default_string(append_to_end)
        return result

    if index > upper:
        start = 0
        end = upper
        start = max(0, start)
        end = min(len(text), end)
        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError("Computed slice indices must be integers")
        return substring_java(text, start, end) + StringUtils.default_string(append_to_end)

    # Abbreviate at the space
    start = 0
    end = index
    start = max(0, start)
    end = min(len(text), end)
    if not isinstance(start, int) or not isinstance(end, int):
        raise ValueError("Computed slice indices must be integers")
    return substring_java(text, start, end) + StringUtils.default_string(append_to_end)