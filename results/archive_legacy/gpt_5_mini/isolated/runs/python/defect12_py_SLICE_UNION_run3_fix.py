@staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY
        if lower is not None and not isinstance(lower, int):
            raise TypeError("lower must be int or None")
        if upper is not None and not isinstance(upper, int):
            raise TypeError("upper must be int or None")
        start = 0 if lower is None else lower
        end = len(text) if upper is None else upper
        length = len(text)
        if start < 0:
            start = 0
        if end < 0:
            end = 0
        if start > length:
            start = length
        if end > length:
            end = length
        index = StringUtils.index_of(text, " ", start)
        if index == -1:
            result = text[start:end]
            if end != length:
                result += StringUtils.default_string(append_to_end)
            return result
        if index > end:
            return text[start:end] + StringUtils.default_string(append_to_end)
        return text[start:index] + StringUtils.default_string(append_to_end)