    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length == 2:
            # Language only
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")
        elif length >= 5:
            # At least language_country
            if locale_str[2] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                # length >= 6
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                # variant may be empty? but spec says variant is arbitrary, could be empty? 
                # In Java, variant can be empty string, but the string representation would not have trailing underscore.
                # So if length == 6, then variant is empty (since after '_' at index 5 there is nothing).
                # However, the original code expects variant from index 6 onwards, which would be empty for length 6.
                # Actually, if length == 6, then locale_str[6:] is '' because slicing beyond length returns empty.
                # So it's fine. But we need to ensure that if length == 6, the variant is empty string.
                # The original code would have raised because of the condition length < 7. Now we allow length >=5.
                # For length == 6, we have language_country_ (trailing underscore) which might be invalid.
                # According to Java Locale, the string format is language + "_" + country + "_" + variant, 
                # and variant cannot be empty? Actually variant can be empty, but then the string should not have the third underscore.
                # So a string with trailing underscore is invalid. We should check that if length >=6 and locale_str[5] == '_', then there must be at least one character after it (i.e., length >=7).
                # Let's implement that: if length == 6, then after the underscore at index 5 there is nothing, so invalid.
                # However, the original code after fixing the condition would still accept length 6 and treat variant as empty.
                # But the spec might not allow empty variant with underscore. We'll follow the original Java behavior.
                # In Java, Locale.toString() returns language + "_" + country + "_" + variant, but if variant is empty, it omits the last underscore.
                # So parsing should not accept trailing underscore. Therefore, we should require that if there is an underscore at position 5, then length must be at least 7 (so variant non-empty).
                # Let's adjust: after checking locale_str[5] == '_', we need to ensure there is at least one character for variant.
                if length < 7:
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
        else:
            # length 3 or 4 (or 1) which are invalid
            raise ValueError(f"Invalid locale format: {locale_str}")