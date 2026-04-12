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
        
        # If length is 2, just language
        if length == 2:
            return Locale(locale_str, "")
        
        # Must have at least 3 characters and underscore at position 2
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If length is 3, that's invalid (e.g., "en_") 
        if length == 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check for double underscore pattern (empty country)
        if length >= 4 and locale_str[3] == '_':
            # Format: language__variant
            # Country is empty, variant starts at index 4
            if length == 4:
                # Only language and double underscore, no variant (e.g., "en__")
                # This is ambiguous; treat as language only? But spec expects variant empty? 
                # We'll treat as language only (country empty, variant empty) but the double underscore suggests variant.
                # However, typical usage expects variant after double underscore.
                # Since length is 4, variant is empty string.
                return Locale(locale_str[0:2], "", "")
            else:
                variant = locale_str[4:]
                return Locale(locale_str[0:2], "", variant)
        
        # Otherwise, we have language_country or language_country_variant
        # Need at least 5 characters for language_country (e.g., en_US)
        if length < 5:
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
            return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])