    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate first two characters as lowercase letters (language)
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if not ('a' <= ch0 <= 'z') or not ('a' <= ch1 <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 2:
            return Locale(locale_str, "", "")
        
        # Must have at least 3 characters if length > 2
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 3:
            # Only language and underscore (e.g., "en_")
            return Locale(locale_str[0:2], "", "")
        
        # Check for double underscore (empty country) pattern
        if locale_str[3] == '_':
            # Format: language__variant
            variant_start = 4
            if variant_start >= length:
                # No variant after double underscore (e.g., "fr__")
                return Locale(locale_str[0:2], "", "")
            variant = locale_str[variant_start:]
            return Locale(locale_str[0:2], "", variant)
        
        # Otherwise, we have a country code (must be exactly 2 uppercase letters)
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if not ('A' <= ch3 <= 'Z') or not ('A' <= ch4 <= 'Z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = locale_str[3:5]
        
        if length == 5:
            return Locale(locale_str[0:2], country, "")
        
        # Check for variant (must start with '_')
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 6:
            # Language, country, and trailing underscore (e.g., "en_US_")
            return Locale(locale_str[0:2], country, "")
        
        variant = locale_str[6:]
        return Locale(locale_str[0:2], country, variant)