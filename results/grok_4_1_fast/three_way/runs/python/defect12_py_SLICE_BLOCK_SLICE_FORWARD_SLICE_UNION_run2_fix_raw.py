    @staticmethod
    def substring_java(s: str, start: int, end: int) -> str:
        """
        Java-like substring(start, end) with bounds checks.

        Python slicing is safe; Java's String.substring throws if end > length.
        """
        if start > end or end > len(s):
            raise IndexError(f"String index out of range: {end}")
        return s[start:end]