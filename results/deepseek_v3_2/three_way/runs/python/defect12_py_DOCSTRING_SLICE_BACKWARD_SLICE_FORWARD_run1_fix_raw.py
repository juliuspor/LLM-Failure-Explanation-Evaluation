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
        # Also ensure upper does not exceed text length
        if upper > len(text):
            upper = len(text)
        # Ensure lower is within bounds; if lower > len(text), set to len(text)
        if lower > len(text):
            lower = len(text)
        # If lower is negative, set to 0
        if lower < 0:
            lower = 0
        # Now upper may have been adjusted, re-check if upper < lower
        if upper < lower:
            upper = lower

        # Find space at or after lower
        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            # No space found, abbreviate at upper
            result = text[:upper]
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result
        
        # Space found
        if index > upper:
            # Space is beyond upper, so cut at upper
            result = text[:upper] + StringUtils.default_string(append_to_end)
            return result
        
        # Space is within bounds, cut at space
        result = text[:index] + StringUtils.default_string(append_to_end)
        return result