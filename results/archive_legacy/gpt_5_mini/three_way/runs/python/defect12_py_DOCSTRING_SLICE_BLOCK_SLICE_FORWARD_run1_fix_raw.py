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
            start = max(0, min(0, len(text)))
            end = max(0, min(upper, len(text)))
            result = substring_java(text, start, end)
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            start = max(0, min(0, len(text)))
            end = max(0, min(upper, len(text)))
            return substring_java(text, start, end) + StringUtils.default_string(append_to_end)

        start = max(0, min(0, len(text)))
        end = max(0, min(index, len(text)))
        return substring_java(text, start, end) + StringUtils.default_string(append_to_end)