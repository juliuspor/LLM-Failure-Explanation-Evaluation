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
        
        # Check if there is a country code (two uppercase letters after first underscore)
        if length >= 5 and locale_str[3] != '_':
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            country = locale_str[3:5]
            if length == 5:
                return Locale(locale_str[0:2], country)
            else:
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                variant = locale_str[6:] if length > 6 else ""
                return Locale(locale_str[0:2], country, variant)
        else:
            # No country code (language__variant format)
            country = ""
            if length == 3:
                # Only language and underscore, no variant (e.g., "fr_")
                return Locale(locale_str[0:2], country)
            else:
                if length >= 4 and locale_str[3] != '_':
                    # Should not happen because we are in else branch where locale_str[3] == '_' or length < 5
                    raise ValueError(f"Invalid locale format: {locale_str}")
                # variant starts after the second underscore (position 4)
                variant = locale_str[4:] if length > 4 else ""
                return Locale(locale_str[0:2], country, variant)