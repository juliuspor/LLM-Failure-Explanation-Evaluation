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
        if lower < 0:
            lower = 0
        if upper < lower:
            upper = lower

        # Try to find a space between lower and upper (inclusive)
        # Prefer the first space at or after lower but before or at upper
        index = StringUtils.index_of(text, " ", lower)
        if index != -1 and index <= upper:
            # Found a space within bounds
            return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)

        # No space found at/after lower within upper. Try to find the last space before or at upper
        last_space = text.rfind(" ", 0, upper + 1)
        if last_space >= lower:
            return substring_java(text, 0, last_space) + StringUtils.default_string(append_to_end)

        # Otherwise, just cut at upper
        result = substring_java(text, 0, upper)
        if upper != text_len:
            result += StringUtils.default_string(append_to_end)
        return result