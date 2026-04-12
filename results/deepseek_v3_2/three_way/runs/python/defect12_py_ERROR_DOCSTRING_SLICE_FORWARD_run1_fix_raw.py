    @staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        # If upper is -1 (no limit), set to length of text
        if upper == -1:
            upper = len(text)
        # Ensure upper is not beyond the string length
        if upper > len(text):
            upper = len(text)
        if upper < lower:
            upper = lower
            # If after adjusting, upper exceeds length, cap it
            if upper > len(text):
                upper = len(text)

        # Find the first space at or after lower
        # Use the original string, not a substring, and search within bounds
        # The search should be from lower to upper (exclusive) because we cannot cut beyond upper.
        # However, the Java original searches from lower to end of string, but then checks if index > upper.
        # We'll mimic that: find space from lower to end of string.
        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            # No space found after lower
            result = substring_java(text, 0, upper)
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result
        
        # Space found at index
        if index > upper:
            # Space is beyond upper, so cut at upper
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)
        
        # Space is within bounds, cut at space
        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)