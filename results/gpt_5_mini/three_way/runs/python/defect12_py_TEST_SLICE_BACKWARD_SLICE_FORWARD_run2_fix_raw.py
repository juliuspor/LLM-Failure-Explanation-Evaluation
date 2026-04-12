@staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        # Interpret -1 as no upper limit
        if upper == -1:
            upper = len(text)

        # Clamp upper to text length
        if upper > len(text):
            upper = len(text)
        if upper < lower:
            upper = lower

        # If lower is beyond length, no abbreviation necessary
        if lower >= len(text):
            return text

        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            # No space found; cut at upper
            end = min(upper, len(text))
            result = substring_java(text, 0, end)
            if end != len(text):
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            end = min(upper, len(text))
            return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)