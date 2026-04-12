    @staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        # If upper is -1 (no limit) or beyond string length, set to length
        if upper == -1 or upper > len(text):
            upper = len(text)
        # Ensure upper is at least lower
        if upper < lower:
            upper = lower
        # If after adjustments upper is beyond length, cap it
        if upper > len(text):
            upper = len(text)

        # Find space after lower
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

        # Space within bounds, abbreviate at space
        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)