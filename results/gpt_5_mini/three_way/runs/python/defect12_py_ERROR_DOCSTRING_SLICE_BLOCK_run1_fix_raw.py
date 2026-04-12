@staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        # Treat upper == -1 as no limit
        if upper == -1 or upper > len(text):
            upper = len(text)
        if upper < lower:
            upper = lower

        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            # ensure end does not exceed length
            end = min(upper, len(text))
            result = substring_java(text, 0, end)
            if end != len(text):
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            end = min(upper, len(text))
            return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)