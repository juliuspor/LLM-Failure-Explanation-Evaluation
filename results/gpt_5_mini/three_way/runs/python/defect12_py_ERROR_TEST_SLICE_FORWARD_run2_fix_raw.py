    @staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        text_len = len(text)
        if upper == -1 or upper > text_len:
            upper = text_len
        if upper < lower:
            upper = lower
        # If lower is beyond length, nothing to abbreviate — return original text
        if lower >= text_len:
            return text

        # find space at or after lower
        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            # no space found; cut at upper
            # ensure slice indices are within bounds
            start = 0
            end = min(upper, text_len)
            result = substring_java(text, start, end)
            if end != text_len:
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            # space found after upper, cut at upper
            start = 0
            end = min(upper, text_len)
            return substring_java(text, start, end) + StringUtils.default_string(append_to_end)

        # space found within bounds; cut at that space
        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)