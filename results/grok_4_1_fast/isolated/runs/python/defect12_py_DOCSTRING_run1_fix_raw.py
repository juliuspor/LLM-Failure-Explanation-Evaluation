@staticmethod
def abbreviate(
    text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
) -> Optional[str]:
    if text is None:
        return None
    if len(text) == 0:
        return StringUtils.EMPTY

    # Normalize bounds
    if upper == -1:
        upper = len(text)
    if upper > len(text):
        upper = len(text)
    if lower < 0:
        lower = 0
    if upper < lower:
        upper = lower

    # Find space in [lower, upper] range
    space_index = StringUtils.index_of(text, " ", lower)
    
    if space_index == -1 or space_index > upper:
        # No suitable space found, truncate at upper
        result = substring_java(text, 0, upper)
    else:
        # Use space boundary
        result = substring_java(text, 0, space_index)
    
    # Append suffix if truncated
    if upper < len(text):
        result += StringUtils.default_string(append_to_end)
    
    return result