    @staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        text_len = len(text)

        # Interpret -1 as no upper limit -> use full length
        if upper == -1 or upper > text_len:
            upper = text_len
        if upper < lower:
            upper = lower

        # If lower is beyond the text length, nothing to abbreviate; return original
        if lower >= text_len:
            return text

        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            # No space found after lower; cut at upper
            # Clamp indices to valid range
            start = max(0, min(0, text_len))
            end = max(start, min(upper, text_len))
            result = substring_java(text, start, end)
            if end != text_len:
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            # space is after upper, cut at upper
            start = 0
            end = max(start, min(upper, text_len))
            return substring_java(text, start, end) + StringUtils.default_string(append_to_end)

        # space found within bounds
        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)