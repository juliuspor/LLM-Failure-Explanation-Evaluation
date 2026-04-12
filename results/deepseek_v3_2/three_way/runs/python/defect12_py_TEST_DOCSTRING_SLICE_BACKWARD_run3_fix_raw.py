    @staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        # Adjust upper if it's -1 or beyond length
        if upper == -1 or upper > len(text):
            upper = len(text)
        # Ensure lower is not greater than upper after adjustment
        if lower > upper:
            lower = upper
        # If lower is beyond length, set it to length (so no abbreviation)
        if lower > len(text):
            lower = len(text)
            upper = len(text)

        # Find space after lower
        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            # No space found
            result = substring_java(text, 0, upper)
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            # Space is beyond upper, cut at upper
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

        # Space found between lower and upper
        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)