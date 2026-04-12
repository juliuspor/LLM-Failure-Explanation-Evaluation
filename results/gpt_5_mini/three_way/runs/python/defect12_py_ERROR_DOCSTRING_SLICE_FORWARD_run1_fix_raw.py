    @staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        text_len = len(text)
        # Treat -1 as no upper bound
        if upper == -1 or upper > text_len:
            upper = text_len
        # ensure upper is at least lower
        if upper < lower:
            upper = lower
        # clamp lower to valid range
        if lower < 0:
            lower = 0

        # find first space at or after lower
        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            # no space found; cut at upper
            end = min(upper, text_len)
            result = substring_java(text, 0, end)
            if end != text_len:
                result += StringUtils.default_string(append_to_end)
            return result

        # if space found after upper, cut at upper
        if index > upper:
            end = min(upper, text_len)
            result = substring_java(text, 0, end)
            if end != text_len:
                result += StringUtils.default_string(append_to_end)
            return result

        # space was found within bounds; cut at that space
        end = min(index, text_len)
        result = substring_java(text, 0, end)
        if end != text_len:
            result += StringUtils.default_string(append_to_end)
        return result