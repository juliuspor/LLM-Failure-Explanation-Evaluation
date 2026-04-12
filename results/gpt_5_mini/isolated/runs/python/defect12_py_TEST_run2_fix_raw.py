@staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        text_len = len(text)

        # Normalize upper: -1 means no limit; clamp to text length
        if upper == -1 or upper > text_len:
            upper = text_len
        if upper < lower:
            upper = lower

        # If lower is beyond the text length, return original text
        if lower >= text_len:
            return text

        # Find a space at or after lower
        index = StringUtils.index_of(text, " ", lower)
        # No space found or space beyond upper: cut at upper
        if index == -1 or index > upper:
            result = substring_java(text, 0, upper)
            if upper != text_len:
                result += StringUtils.default_string(append_to_end)
            return result

        # Found a space within bounds: cut at that space
        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)