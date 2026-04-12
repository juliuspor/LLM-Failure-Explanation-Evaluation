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

        # If lower is beyond the string length, we cannot find a space.
        # In that case, we should treat the whole string as the result,
        # but we must still respect the upper bound.
        # However, after adjusting upper, if upper > len(text) (because lower > len(text)),
        # we need to clamp upper to len(text) to avoid substring_java exception.
        if lower > len(text):
            # No space can be found, and the substring will be the whole string.
            # But we must still apply upper, which is at least lower, so upper > len(text).
            # So we set upper to len(text) to avoid index error.
            upper = len(text)
            # Now we can proceed; index_of will return -1 because lower > len(text).
            # The code below will handle -1 correctly because upper is now len(text).

        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            result = substring_java(text, 0, upper)
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)