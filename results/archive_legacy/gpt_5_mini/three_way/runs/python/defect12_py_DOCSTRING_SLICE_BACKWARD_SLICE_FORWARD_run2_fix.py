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
        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            start = 0
            end = min(upper, len(text))
            return substring_java(text, start, end) + (StringUtils.default_string(append_to_end) if end != len(text) else StringUtils.EMPTY)
        if index > upper:
            start = 0
            end = min(upper, len(text))
            return substring_java(text, start, end) + StringUtils.default_string(append_to_end)
        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)