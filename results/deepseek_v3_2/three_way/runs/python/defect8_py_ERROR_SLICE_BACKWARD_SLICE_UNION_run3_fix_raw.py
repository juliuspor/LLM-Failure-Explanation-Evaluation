    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 2:
            return Locale(locale_str, "")
        
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check if there is a country code (two uppercase letters) after the first underscore
        if length >= 5 and locale_str[3] >= 'A' and locale_str[3] <= 'Z' and locale_str[4] >= 'A' and locale_str[4] <= 'Z':
            # Format: language_country or language_country_variant
            country = locale_str[3:5]
            if length == 5:
                return Locale(locale_str[0:2], country)
            else:
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                variant = locale_str[6:] if length > 6 else ""
                return Locale(locale_str[0:2], country, variant)
        else:
            # Format: language__variant (double underscore, no country)
            if length >= 4 and locale_str[3] == '_':
                variant = locale_str[4:] if length > 4 else ""
                return Locale(locale_str[0:2], "", variant)
            else:
                # Single underscore but no valid country code and not a double underscore
                raise ValueError(f"Invalid locale format: {locale_str}")