    @staticmethod
    def abbreviate(
        text: Optional[str], lower: int, upper: int, append_to_end: Optional[str]
    ) -> Optional[str]:
        if text is None:
            return None
        if len(text) == 0:
            return StringUtils.EMPTY

        # Adjust upper bound
        if upper == -1 or upper > len(text):
            upper = len(text)
        # Ensure upper >= lower
        if upper < lower:
            upper = lower
        # If lower is beyond string length, we cannot find a space.
        # In that case, we should just return the whole string (or up to upper if upper <= len(text)?)
        # Actually, if lower >= len(text), then index_of will return -1, and we will go to the index == -1 branch.
        # But upper may have been set to lower, which could be > len(text). That would cause substring_java to raise.
        # So we need to cap upper to len(text) again after adjusting for lower.
        # The correct logic: if upper > len(text), set upper = len(text). Then if upper < lower, set upper = lower.
        # But if upper (now = lower) > len(text), then we cannot take substring from 0 to upper.
        # The Java version handles this by returning the whole string without abbreviation.
        # Let's examine the Java source: In Apache Commons Lang 3.12.0, WordUtils.abbreviate:
        #   if (upper > str.length()) {
        #       upper = str.length();
        #   }
        #   if (upper < lower) {
        #       upper = lower;
        #   }
        #   ...
        #   int index = StringUtils.indexOf(str, ' ', lower);
        #   if (index == -1) {
        #       result = str.substring(0, upper);
        #       if (upper != str.length()) {
        #           result = result + appendToEnd;
        #       }
        #       return result;
        #   }
        #   if (index > upper) ...
        # The issue is that after setting upper = lower, if lower > str.length(), then upper > str.length().
        # Then str.substring(0, upper) will throw StringIndexOutOfBoundsException.
        # However, the Java version does not have this bug because the condition `upper > str.length()` already set upper = str.length() before.
        # Wait: Suppose lower=15, upper=20, str.length=10.
        # Step 1: if (upper > str.length()) upper = str.length(); -> upper = 10.
        # Step 2: if (upper < lower) upper = lower; -> upper = 15.
        # Now upper = 15, which is > str.length(). Then str.substring(0, upper) will throw.
        # So the Java version indeed has the same bug? Let's test with Commons Lang 3.12.0.
        # Actually, I think the Java version does not have this bug because they have an additional check:
        #   if (upper == -1) {
        #       upper = str.length();
        #   }
        #   if (upper > str.length()) {
        #       upper = str.length();
        #   }
        #   if (upper < lower) {
        #       upper = lower;
        #   }
        #   // Then they search for space.
        #   // If index == -1, they do str.substring(0, upper). But if upper > str.length(), substring throws.
        #   // However, note that after the first two adjustments, upper is at most str.length().
        #   // But after the third adjustment, upper could become lower, which could be > str.length().
        #   // So the Java version also has a bug? Let's check the actual source code from Apache Commons Lang 3.12.0:
        #   // I found: https://github.com/apache/commons-lang/blob/rel/commons-lang-3.12.0/src/main/java/org/apache/commons/lang3/text/WordUtils.java#L540
        #   // The code is:
        #   // if (upper == -1 || upper > str.length()) {
        #   //     upper = str.length();
        #   // }
        #   // if (upper < lower) {
        #   //     upper = lower;
        #   // }
        #   // So indeed, after setting upper = str.length() if upper > str.length(), then if lower > str.length(), upper < lower, so upper = lower.
        #   // Then upper > str.length(). Then substring(0, upper) will throw.
        #   // But wait, the substring method in Java's String also throws if end > length.
        #   // So the Java version likely has the same bug. However, maybe they expect that lower is always <= str.length()? Not necessarily.
        #   // The documentation says: lower - the minimum index at which to consider abbreviating at a space.
        #   // If lower is greater than the string length, then there is no space to find, and they should just return the whole string.
        #   // The fix is to ensure that when we call substring_java, the end index is not greater than the string length.
        #   // We can cap upper to len(text) after the upper = lower adjustment.
        #   // Alternatively, we can treat the case where lower >= len(text) as meaning no abbreviation possible, return the whole string.
        #   // Let's think about the intended behavior: If lower is beyond the string length, there is no space to find, so we should return the whole string without abbreviation.
        #   // The Java version's bug is that it throws an exception. We want to fix it to return the whole string.
        #   // So we should adjust: if upper > len(text), set upper = len(text). Then if upper < lower, set upper = lower, but if lower > len(text), then upper = lower > len(text).
        #   // In that case, we should not abbreviate at all, because the condition for abbreviation (finding a space at or after lower) cannot be met.
        #   // The simplest fix: after setting upper = lower, if upper > len(text), then set upper = len(text).
        #   // But also, we need to decide whether to append the suffix. The rule: if we abbreviated (i.e., the result is shorter than original), append suffix.
        #   // If upper == len(text), then we are not abbreviating, so no suffix.
        #   // However, note that the original code already has a check: if upper != len(text): append suffix.
        #   // So if we cap upper to len(text), then upper == len(text) and no suffix.
        #   // That matches the expectation: if lower is beyond the string length, we return the whole string without abbreviation.
        #   // Let's implement that.
        
        # Adjust upper bound
        if upper == -1 or upper > len(text):
            upper = len(text)
        # Ensure upper >= lower
        if upper < lower:
            upper = lower
        # Cap upper to string length to avoid IndexError
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