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

        # If lower is beyond the string length, no space can be found.
        # In this case, we should treat it as if no space was found.
        if lower >= len(text):
            index = -1
        else:
            index = StringUtils.index_of(text, " ", lower)
        
        if index == -1:
            # No space found, abbreviate at upper.
            # But if upper is beyond the string length, just return the whole string.
            if upper >= len(text):
                return text
            result = substring_java(text, 0, upper)
            result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)