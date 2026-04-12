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

        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            # No space found after lower: cut at upper
            if upper >= text_len:
                return text
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

        if index > upper:
            if upper >= text_len:
                return text
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)
