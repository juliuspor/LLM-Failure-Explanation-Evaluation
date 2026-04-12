    @staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        # If upper is -1 (no limit) or beyond the string length, set it to the string length
        if upper == -1 or upper > len(text):
            upper = len(text)
        # Ensure upper is at least lower
        if upper < lower:
            upper = lower
        # If after adjustments, upper is beyond the string length, set it to the string length again
        if upper > len(text):
            upper = len(text)
        # Also adjust lower if it is beyond the string length
        if lower > len(text):
            lower = len(text)
        # Now, if lower > upper after adjustments, set upper = lower (should not happen, but safe)
        if lower > upper:
            upper = lower

        # Find a space at or after lower
        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            # No space found, abbreviate at upper
            result = substring_java(text, 0, upper)
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result

        # Space found, check if it's beyond upper
        if index > upper:
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

        # Space found within bounds, abbreviate at the space
        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)