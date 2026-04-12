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

        # Prefer a space between lower and upper (inclusive). If found, cut there.
        space_to_wrap_at = text.rfind(" ", lower, upper + 1)
        if space_to_wrap_at >= lower:
            return substring_java(text, 0, space_to_wrap_at) + StringUtils.default_string(append_to_end)

        # No space before upper — look for a space at or after lower
        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            # No space found at or after lower
            result = substring_java(text, 0, upper)
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result

        # Found a space after upper (index > upper) or between upper and end
        if index > upper:
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

        # index is between lower and upper (shouldn't happen because we checked rfind), but handle defensively
        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)