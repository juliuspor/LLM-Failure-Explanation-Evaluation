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

        # If upper is beyond the string length, no abbreviation is needed.
        if upper >= len(text):
            # Check if lower is beyond length? Actually, if upper >= len(text) and lower <= upper,
            # we can just return the whole string because we are not cutting.
            # But we must still consider the space search? The original Java code:
            # If upper >= str.length(), it returns the whole string without appending.
            # However, the Java code also searches for a space starting at lower.
            # If lower is beyond the string length, indexOf returns -1.
            # Then it returns substring(0, upper) which is the whole string.
            # So we can safely return the whole string.
            return text

        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            result = substring_java(text, 0, upper)
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)