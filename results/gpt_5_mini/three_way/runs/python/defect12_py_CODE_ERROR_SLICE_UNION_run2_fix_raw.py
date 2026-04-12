@staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        text_len = len(text)

        # Normalize lower
        if lower < 0:
            lower = 0
        if lower > text_len:
            lower = text_len

        # Handle upper == -1 as no limit
        if upper == -1:
            upper = text_len

        # Ensure upper is at least lower
        if upper < lower:
            upper = lower

        # Clamp upper to text length
        if upper > text_len:
            upper = text_len

        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            result = substring_java(text, 0, upper)
            if upper != text_len:
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)