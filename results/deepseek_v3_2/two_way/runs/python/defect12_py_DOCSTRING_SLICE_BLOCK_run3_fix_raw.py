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
        # In that case, we should just return the whole string (or up to upper if upper is smaller).
        # But note: if lower > len(text), then substring_java(0, upper) would raise an error
        # because start (0) is fine, but end (upper) may be less than start? Actually upper is set to lower if lower > upper.
        # However, the main issue is that we might call substring_java with start > len(s) if lower > len(text) and we use lower as start.
        # But we never use lower as start; we only use 0 as start. So the only problematic case is when lower > len(text) and we call substring_java(0, upper) where upper = lower (since upper < lower condition) and lower > len(text).
        # Then substring_java(0, upper) with upper > len(s) will raise IndexError because end > len(s).
        # So we need to ensure that upper does not exceed len(text) after adjusting for lower.
        # Actually, we already set upper = len(text) if upper == -1 or upper > len(text). But if upper < lower, we set upper = lower.
        # So if lower > len(text), then upper becomes lower (which is > len(text)). Then substring_java(0, upper) will fail.
        # Therefore, we should cap upper at len(text) after the upper < lower adjustment.
        # Let's restructure: first, handle the case where lower > len(text). In that case, there is no space after lower, so we should return text up to upper (or whole text if upper is -1). But if lower > len(text), the string is shorter than lower, so we cannot abbreviate at a space after lower. The original Java code would return the substring from 0 to upper (with append if needed). However, if lower > len(text), the indexOf will return -1, and we go to the branch result = substring_java(text, 0, upper). But if upper is set to lower (because upper < lower) and lower > len(text), then upper > len(text) and substring_java will throw. So we need to ensure upper does not exceed len(text).
        # The fix: after adjusting upper for -1 and > len(text), then after the upper < lower adjustment, we should cap upper at len(text) again.
        # Alternatively, we can check if lower > len(text) and handle it early.
        # Let's adopt the early handling: if lower >= len(text), then there is no space after lower, so we can just return the whole string (or up to upper if upper is smaller). But we must still consider upper.
        # Actually, the Java implementation does not have this check; it would call indexOf with start index beyond length, which returns -1, then proceed to substring(0, upper). If upper is adjusted to lower (which is > length), substring throws StringIndexOutOfBoundsException. So the Java version also has a bug? Let's examine the original Java code (from Apache Commons Lang). I think the Java version does not have this bug because substring(0, upper) with upper > length throws. But the Java version likely ensures upper is not greater than length. Let's look at the Commons Lang 3.12.0 source: In WordUtils.abbreviate, they have:
        # if (upper == -1 || upper > str.length()) {
        #     upper = str.length();
        # }
        # if (upper < lower) {
        #     upper = lower;
        # }
        # Then they call str.indexOf(' ', lower). If lower > str.length(), indexOf returns -1. Then they do:
        # if (index == -1) {
        #     result = str.substring(0, upper);
        #     if (upper != str.length()) {
        #         result += appendToEnd;
        #     }
        # }
        # But if upper was set to lower (because upper < lower) and lower > str.length(), then upper > str.length(), and substring(0, upper) throws. So indeed there is a bug in the Java version as well? Wait, the condition upper < lower only sets upper = lower if upper < lower. If lower > str.length() and upper is -1, then upper becomes str.length() (since upper > str.length() is true). Then upper < lower? str.length() < lower, so yes, upper < lower, so upper = lower. Then upper > str.length(). So bug.
        # Therefore, we need to fix it. The fix is to ensure that after setting upper = lower, we still cap upper at len(text). Because if lower > len(text), the maximum we can go is len(text). So we should do: if upper > len(text): upper = len(text).
        # Let's implement that.
        # After adjusting upper for -1 and > len(text), and after upper < lower adjustment, we should cap upper at len(text).
        # But note: if upper is set to lower and lower > len(text), then upper > len(text). So we need to cap.
        # So add: if upper > len(text): upper = len(text)
        # However, we already set upper = len(text) if upper > len(text) earlier. But after upper = lower, it may become > len(text). So we need to re-check.
        # Let's restructure the upper adjustment:
        # 1. If upper == -1 or upper > len(text): upper = len(text)
        # 2. If upper < lower: upper = lower
        # 3. If upper > len(text): upper = len(text)   (this handles the case where lower > len(text))
        # Alternatively, we can combine: after step 2, set upper = min(upper, len(text)).
        # But note: if lower > len(text), then upper = lower > len(text), so min will bring it back to len(text). That's fine.
        # However, we must also consider that if lower > len(text), the indexOf will return -1, and we will return substring(0, upper) which is now substring(0, len(text)) i.e., the whole string. That seems correct: if the lower bound is beyond the string, we cannot abbreviate at a space, so we return the whole string (or up to upper if upper is smaller, but upper is len(text) so whole string). And we should not append append_to_end because upper == len(text). That matches the condition: if upper != len(text) then append.
        # So the fix is to add: upper = min(upper, len(text)) after the upper < lower adjustment.
        # But we don't have min imported; we can use built-in min.
        # Let's implement.

        # Step 1: adjust upper for -1 and out-of-range
        if upper == -1 or upper > len(text):
            upper = len(text)
        # Step 2: ensure upper is not less than lower
        if upper < lower:
            upper = lower
        # Step 3: ensure upper does not exceed string length (important when lower > len(text))
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