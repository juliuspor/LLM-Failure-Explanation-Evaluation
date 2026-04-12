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
        
        # Must have at least one underscore after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check if country is present (next two characters are uppercase letters)
        if length >= 5 and locale_str[3] >= 'A' and locale_str[3] <= 'Z' and locale_str[4] >= 'A' and locale_str[4] <= 'Z':
            # Format: language_COUNTRY or language_COUNTRY_variant
            country = locale_str[3:5]
            if length == 5:
                return Locale(locale_str[0:2], country)
            else:
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                variant = locale_str[6:] if length > 6 else ""
                return Locale(locale_str[0:2], country, variant)
        else:
            # Format: language__variant (empty country)
            if length == 3:
                # Only language and underscore, no variant
                return Locale(locale_str[0:2], "")
            # Check for second underscore
            if length >= 4 and locale_str[3] == '_':
                variant = locale_str[4:] if length > 4 else ""
                return Locale(locale_str[0:2], "", variant)
            else:
                # Single underscore but no valid country or second underscore
                raise ValueError(f"Invalid locale format: {locale_str}")