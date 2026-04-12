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
        
        # Must have at least 3 characters for separator
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 3:
            # Only language and underscore (e.g., "en_") -> treat as language only
            return Locale(locale_str[0:2], "")
        
        # Now we have at least 4 characters: "xx_" + something
        # Check if the next part is country (uppercase letters) or another underscore (empty country)
        if length >= 5 and locale_str[3] != '_' and locale_str[4] != '_':
            # Possibly a country code (two uppercase letters)
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if 'A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z':
                # Valid country code
                if length == 5:
                    return Locale(locale_str[0:2], locale_str[3:5])
                else:
                    if locale_str[5] != '_':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    # Country and variant
                    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
            # If not uppercase letters, fall through to treat as variant
        
        # If we reach here, either country is empty (two underscores) or the characters after first underscore are not a valid country code.
        # The format is language + underscore + variant (country empty).
        # The variant starts after the first underscore (or after the second underscore if country empty).
        # We need to find where the variant starts.
        # If there is a second underscore immediately after the first, country is empty.
        if locale_str[3] == '_':
            # Empty country, variant starts at index 4
            return Locale(locale_str[0:2], "", locale_str[4:])
        else:
            # No country code, the rest after the first underscore is the variant
            return Locale(locale_str[0:2], "", locale_str[3:])