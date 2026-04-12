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

        # If lower is beyond the string length, there is no space to find.
        # In such case, we should treat it as if no space was found.
        # Also, we must ensure that the substring_java call does not exceed bounds.
        # The Java original uses String.indexOf which returns -1 if start index >= length.
        # We'll mimic that by checking if lower >= len(text).
        if lower >= len(text):
            # No space can be found, so we abbreviate at upper (which is >= lower).
            # But upper may also be beyond length; we need to clamp it.
            effective_upper = min(upper, len(text))
            result = substring_java(text, 0, effective_upper)
            if effective_upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result

        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            result = substring_java(text, 0, upper)
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)