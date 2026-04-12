    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate language part (first two characters must be lowercase letters)
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 2:
            return Locale(locale_str, "")
        
        # At least 3 characters, check for separator
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 3:
            # Only language and underscore (e.g., "en_") -> treat as language only
            return Locale(locale_str[0:2], "")
        
        # Now we have at least 4 characters: language + "_" + something
        # Check if the next part is a country (two uppercase letters) or empty country (another underscore)
        if length >= 5 and locale_str[3] != '_' and locale_str[4] != '_':
            # Possibly a country code: two uppercase letters
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 >= 'A' and ch3 <= 'Z' and ch4 >= 'A' and ch4 <= 'Z':
                # Valid country code
                if length == 5:
                    return Locale(locale_str[0:2], locale_str[3:5])
                else:
                    if locale_str[5] != '_':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    # Country and variant
                    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
            else:
                # Not uppercase letters, so treat as variant (country empty)
                # The format is language + "_" + variant (country empty)
                # This handles cases like "fr__POSIX" where country is empty.
                # Actually, if ch3 is not uppercase, we should treat everything after the first underscore as variant.
                # But the spec says double underscore indicates empty country.
                # So we need to check if the character after the first underscore is another underscore.
                pass
        
        # If we reach here, either length is 4, or the pattern doesn't match two uppercase letters.
        # Check for double underscore (empty country) followed by variant.
        if length >= 4 and locale_str[3] == '_':
            # Double underscore: language, empty country, variant
            # Example: "fr__POSIX" -> language="fr", country="", variant="POSIX"
            return Locale(locale_str[0:2], "", locale_str[4:])
        
        # If length is 4, then we have language + "_" + single character (e.g., "en_A")
        # This could be a malformed country code (should be two uppercase) or a variant.
        # According to Java Locale, a single character after underscore is not valid.
        # We'll treat it as a variant (country empty) for robustness.
        # But the original code expected a two-letter country, so we need to decide.
        # The bug diagnosis specifically mentions double underscore, so we handle that.
        # For other cases, we can raise an error or adapt.
        # Let's follow the original logic: if length >=5 and country not uppercase, raise error.
        # However, we already handled the double underscore case.
        # If we get here, it's an invalid format.
        raise ValueError(f"Invalid locale format: {locale_str}")