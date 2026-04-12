    @staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        if upper == -1 or upper > len(text):
            upper = len(text)
        if upper < lower:
            upper = lower

        # Ensure lower and upper are within bounds for substring_java
        # substring_java will raise IndexError if start > len(text) or end > len(text)
        # but we have already adjusted upper to len(text) if needed.
        # However, lower could still be > len(text) after upper adjustment.
        # If lower > len(text), set lower = len(text) to avoid IndexError.
        if lower > len(text):
            lower = len(text)
        # Also ensure upper >= lower after adjusting lower.
        if upper < lower:
            upper = lower

        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            result = substring_java(text, 0, upper)
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)