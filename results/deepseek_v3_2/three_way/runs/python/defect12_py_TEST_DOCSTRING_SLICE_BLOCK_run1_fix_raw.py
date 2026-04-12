    @staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        """
        Abbreviate `text`, preferably at a word boundary.

        The function looks for a space character at or after `lower`. If a space
        is found before `upper`, the result ends at that space; otherwise the
        result is cut at `upper`. When an abbreviation occurs, `append_to_end`
        (for example `"..."`) is appended.

        Args:
            text: Input string. If None, returns None.
            lower: Minimum index at which to consider abbreviating at a space.
            upper: Maximum end index for the abbreviated string. Use `-1` for no limit.
            append_to_end: Suffix to append when the text is abbreviated.

        Returns:
            The abbreviated string (or None if `text` is None).
        """
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        # If upper is -1, treat as no limit -> set to length of text
        if upper == -1:
            upper = len(text)
        # If upper is beyond length, clamp to length
        if upper > len(text):
            upper = len(text)
        # Ensure lower is not greater than upper after adjustments
        if lower > upper:
            lower = upper
        # If lower is beyond length, set to length (so no abbreviation)
        if lower > len(text):
            lower = len(text)
            # If lower equals length, then no abbreviation needed
            if lower == len(text):
                return text
        
        # Find space at or after lower
        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            # No space found, abbreviate at upper
            result = substring_java(text, 0, upper)
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result
        
        if index > upper:
            # Space found but beyond upper, abbreviate at upper
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)
        
        # Space found within bounds, abbreviate at space
        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)