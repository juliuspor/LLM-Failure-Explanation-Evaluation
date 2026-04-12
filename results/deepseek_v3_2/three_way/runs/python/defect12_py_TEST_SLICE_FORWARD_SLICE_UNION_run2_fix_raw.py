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

        # If lower is beyond the string length, no space can be found.
        if lower >= len(text):
            result = text[:upper]
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result

        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            result = text[:upper]
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            return text[:upper] + StringUtils.default_string(append_to_end)

        return text[:index] + StringUtils.default_string(append_to_end)