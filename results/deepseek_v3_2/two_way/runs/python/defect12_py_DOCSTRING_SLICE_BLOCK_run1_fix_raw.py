    @staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        """
        Abbreviate `text`, preferably at a word boundary.

        The function looks for a space character at or after `lower`. If a space
        is found before `upper`, the result ends at that space; otherwise the
        result is cut at `upper`. When an abbreviation occurs, `append_to_end`
        (for example `"..."`) is appended.

        Args:
            text: Input string. If None, returns None.
            lower: Minimum index at which to consider abbreviating at a space.
            upper: Maximum end index for the abbreviated string. Use `-1` for no limit.
            append_to_end: Suffix to append when the text is abbreviated.

        Returns:
            The abbreviated string (or None if `text` is None).
        """
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        if upper == -1 or upper > len(text):
            upper = len(text)
        if upper < lower:
            upper = lower
        # Ensure upper does not exceed string length after adjustment
        if upper > len(text):
            upper = len(text)

        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            result = substring_java(text, 0, upper)
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)