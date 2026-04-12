    @staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        # If upper is -1 (no limit) or beyond string length, set to string length
        if upper == -1 or upper > len(text):
            upper = len(text)
        # Ensure upper is at least lower
        if upper < lower:
            upper = lower
        
        # If lower is beyond string length, we cannot find a space; treat as no space.
        # Also, if lower is beyond the string length, we should just return the whole string
        # (or up to upper if upper is within bounds). But note that upper may have been adjusted.
        # Actually, the Java behavior: if lower > length, then indexOf returns -1, and we go to the no-space branch.
        # However, substring_java will raise IndexError if end > length. So we must ensure upper <= length.
        # Since we already set upper = len(text) if upper > len(text), but then we may have set upper = lower,
        # which could be > len(text). So we need to cap upper at len(text) after adjusting for lower.
        # Let's re-evaluate: after the above adjustments, upper could be > len(text) if lower > len(text).
        # So we need to cap upper to len(text) again.
        if upper > len(text):
            upper = len(text)
        
        # Find space starting at lower, but only if lower is within bounds.
        if lower >= len(text):
            index = -1
        else:
            index = StringUtils.index_of(text, " ", lower)
        
        if index == -1:
            # No space found: abbreviate at upper.
            # But if upper is beyond length, we can just return the whole string without append.
            if upper >= len(text):
                # No abbreviation needed because we are taking the whole string.
                return text
            result = substring_java(text, 0, upper)
            result += StringUtils.default_string(append_to_end)
            return result
        
        if index > upper:
            # Space found but beyond upper, so abbreviate at upper.
            # Again, if upper is beyond length, return whole string without append? Actually upper is capped.
            if upper >= len(text):
                return text
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)
        
        # Space found within bounds: abbreviate at space.
        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)