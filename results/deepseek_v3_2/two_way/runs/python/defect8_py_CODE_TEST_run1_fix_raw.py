    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate first two characters are lowercase letters
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 2:
            return Locale(locale_str, "")
        
        # Must have at least 3 characters and third character must be underscore
        if length < 3 or locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check if country code is empty (two underscores)
        if length >= 4 and locale_str[3] == '_':
            # Format: language__variant
            # Country is empty, variant starts after the second underscore
            if length == 4:
                # Only language and two underscores, no variant? Actually invalid because variant missing.
                # But we can treat as language only? According to Java Locale, "fr__" is invalid.
                # We'll raise error because variant is expected after second underscore.
                raise ValueError(f"Invalid locale format: {locale_str}")
            # variant starts at index 4
            variant = locale_str[4:]
            return Locale(locale_str[0:2], "", variant)
        else:
            # Format: language_country or language_country_variant
            if length < 5:
                # Need at least 5 chars for language_country (e.g., en_US)
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                variant = locale_str[6:] if length > 6 else ""
                return Locale(locale_str[0:2], locale_str[3:5], variant)