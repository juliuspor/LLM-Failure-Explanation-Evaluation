    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate first two characters are lowercase letters (language code)
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
        
        # Now we have at least 4 characters: "xx_" + something
        # Check if the next part is a country code (two uppercase letters) or another underscore (empty country)
        if length >= 5 and locale_str[3] != '_' and locale_str[4] != '_':
            # Possibly a country code: two uppercase letters
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
            # If not two uppercase letters, fall through to treat as variant (or error)
        
        # If we reach here, either:
        # - length == 4: "xx_y" (single character after underscore) -> treat as variant? Actually invalid per Java.
        # - length >=5 but country code not valid (e.g., first char after underscore is '_' or not uppercase)
        # We need to handle the case where country is empty and variant follows immediately after double underscore.
        # That means after the first underscore, we have another underscore.
        # So we check if the character at index 3 is '_' (double underscore).
        if length >= 4 and locale_str[3] == '_':
            # Double underscore: language__variant
            # The country is empty, variant starts at index 4
            return Locale(locale_str[0:2], "", locale_str[4:])
        
        # If we have a single underscore and the next part is not a valid country code,
        # and not a double underscore, then it could be a variant that doesn't start with uppercase letters?
        # According to Java's Locale, the format is language_country_variant, where country must be two uppercase letters
        # or missing. So if we have language_X... where X is not uppercase letter, it's invalid.
        # However, we already checked that if length>=5 and ch3,ch4 are uppercase, we handled.
        # For length==4, we have "xx_y" which is invalid because country must be two letters or empty.
        # So we raise an error.
        raise ValueError(f"Invalid locale format: {locale_str}")