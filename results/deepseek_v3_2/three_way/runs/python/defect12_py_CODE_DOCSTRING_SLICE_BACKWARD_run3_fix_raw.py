    @staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        # Adjust upper bound: -1 means no limit -> set to text length
        if upper == -1 or upper > len(text):
            upper = len(text)
        # Ensure lower is not beyond text length
        if lower > len(text):
            lower = len(text)
        # Now ensure upper >= lower (but upper already <= len(text) and lower <= len(text))
        if upper < lower:
            upper = lower
        # After adjustments, if upper > len(text) (should not happen) cap it
        if upper > len(text):
            upper = len(text)

        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            result = substring_java(text, 0, upper)
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)