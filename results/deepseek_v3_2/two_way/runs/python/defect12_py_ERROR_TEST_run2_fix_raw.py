    @staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        # If lower is greater than the string length, return the whole string.
        if lower > len(text):
            lower = len(text)
        if upper == -1 or upper > len(text):
            upper = len(text)
        if upper < lower:
            upper = lower

        # Find a space at or after lower, but only within the string bounds.
        # If lower is at or beyond the end, index_of will return -1.
        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            result = substring_java(text, 0, upper)
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)