    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        # Remove any leading/trailing whitespace
        locale_str = locale_str.strip()
        length = len(locale_str)
        
        # Handle language only (e.g., "en")
        if length == 2:
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 >= 'a' and ch0 <= 'z' and ch1 >= 'a' and ch1 <= 'z':
                return Locale(locale_str, "")
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Must have at least 3 characters for language + separator
        if length < 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate first two characters as lowercase letters
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check separator after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Now we have language_ ...
        # Cases:
        # 1. language_XX (country only) -> length 5, positions 3,4 are uppercase letters
        # 2. language_XX_variant (country + variant) -> length >= 7, positions 3,4 uppercase, underscore at 5
        # 3. language__variant (empty country) -> length >= 4, underscore at 2, underscore at 3? Actually double underscore.
        #    After first underscore, if next char is '_', then country is empty.
        
        # Check if country is empty (double underscore)
        if length >= 4 and locale_str[3] == '_':
            # language__variant
            # variant starts at position 4
            variant = locale_str[4:] if length > 4 else ""
            return Locale(locale_str[0:2], "", variant)
        
        # Otherwise, expect a country code (two uppercase letters)
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = locale_str[3:5]
        
        if length == 5:
            return Locale(locale_str[0:2], country, "")
        else:
            # Must have underscore after country
            if locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = locale_str[6:] if length > 6 else ""
            return Locale(locale_str[0:2], country, variant)