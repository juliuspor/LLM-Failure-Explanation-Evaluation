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

        # Ensure lower is within bounds for searching
        if lower > text_len:
            lower = text_len

        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            # ensure upper does not exceed text length
            end = upper if upper <= text_len else text_len
            result = substring_java(text, 0, end)
            if upper != text_len:
                result += StringUtils.default_string(append_to_end)
            return result

        # Clamp index to not exceed text length
        if index > text_len:
            index = text_len

        if index > upper:
            end = upper if upper <= text_len else text_len
            return substring_java(text, 0, end) + StringUtils.default_string(append_to_end)

        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)