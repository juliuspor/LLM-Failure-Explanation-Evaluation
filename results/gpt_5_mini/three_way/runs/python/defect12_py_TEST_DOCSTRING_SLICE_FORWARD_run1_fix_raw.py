@staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        text_len = len(text)
        # Normalize upper: -1 means no limit
        if upper == -1 or upper > text_len:
            upper = text_len
        if upper < lower:
            upper = lower

        # If lower is beyond the text length, no abbreviation should occur
        if lower >= text_len:
            return text

        # Find first space at or after lower
        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            # No space found; cut at upper
            # Ensure indices are within bounds
            start = max(0, min(0, text_len))
            end = max(0, min(upper, text_len))
            result = substring_java(text, start, end)
            if end != text_len:
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            start = 0
            end = max(0, min(upper, text_len))
            return substring_java(text, start, end) + StringUtils.default_string(append_to_end)

        # index is within [lower, upper]
        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)