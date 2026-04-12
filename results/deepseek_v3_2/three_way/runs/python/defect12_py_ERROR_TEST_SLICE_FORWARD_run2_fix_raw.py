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

        # If lower is beyond the string length, we cannot abbreviate.
        # The Java version returns the original string (or empty if upper is also beyond?).
        # According to the test, when lower > length, we should return the original string.
        # But we must also consider the upper bound.
        # Actually, the Java version of WordUtils.abbreviate handles this by:
        # - If lower > length, then the indexOf search returns -1, and we go to the branch where result = substring(0, upper).
        # However, substring_java throws IndexError if start > len(s). So we need to adjust.
        # The fix: before calling substring_java, ensure start is within bounds.
        # In the case where lower > len(text), index will be -1, and we go to the first branch.
        # Then we call substring_java(text, 0, upper). But upper may have been set to lower (if upper < lower) or to len(text).
        # If lower > len(text), then upper could be lower (if upper < lower) or len(text) (if upper > len(text)).
        # In the test, lower=15, upper=20, text length=10. So upper > len(text) => upper = len(text)=10.
        # Then upper < lower? 10 < 15 => true, so upper = lower = 15.
        # Now upper = 15, which is > len(text). Then substring_java(text, 0, 15) will throw because end > len(s).
        # So we need to cap upper to len(text) before calling substring_java.
        # Actually, we already have: if upper == -1 or upper > len(text): upper = len(text).
        # But after that, we have: if upper < lower: upper = lower. This can set upper back to a value > len(text).
        # That's the bug: we should not set upper to lower if lower > len(text). Instead, we should cap upper to len(text).
        # The correct logic: after adjusting upper based on -1 or > len, we should ensure upper does not exceed len(text).
        # But the condition upper < lower is from the Java code: if (upper < lower) { upper = lower; }
        # However, the Java substring method throws if end > length. So we need to protect against that.
        # The Java version likely does not throw because it uses StringUtils.substring which returns the string up to length.
        # But our substring_java throws. So we need to adjust.
        # Let's change: after setting upper = lower, we should cap upper to len(text).
        # Alternatively, modify substring_java to be safe like Java's StringUtils.substring? But the spec says substring_java mimics Java's substring.
        # The bug is that we allow upper to exceed length after the upper < lower adjustment.
        # So fix: after adjusting upper, ensure upper <= len(text).
        # Also, we need to ensure that start index (0) is always valid.
        # So:
        if upper > len(text):
            upper = len(text)
        # Now proceed.
        index = StringUtils.index_of(text, " ", lower)
        if index == -1:
            result = substring_java(text, 0, upper)
            if upper != len(text):
                result += StringUtils.default_string(append_to_end)
            return result

        if index > upper:
            return substring_java(text, 0, upper) + StringUtils.default_string(append_to_end)

        return substring_java(text, 0, index) + StringUtils.default_string(append_to_end)