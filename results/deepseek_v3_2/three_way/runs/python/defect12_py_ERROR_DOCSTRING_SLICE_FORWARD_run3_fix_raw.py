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

        # Find space at or after lower
        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            # No space found after lower
            result = substring_java(text, 0, upper)
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result
        else:
            # Space found
            if index > upper:
                # Space beyond upper, cut at upper
                return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)
            else:
                # Space within bounds, cut at space
                return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)