    @staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        # If upper is -1, treat as no limit -> set to length of text
        if upper == -1:
            upper = len(text)
        # Ensure upper is not less than lower
        if upper < lower:
            upper = lower
        # Also ensure upper does not exceed text length (should be already, but safe)
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