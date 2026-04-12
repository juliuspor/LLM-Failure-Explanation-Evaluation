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
        
        if length == 3:
            # Only language and underscore (e.g., "en_")
            return Locale(locale_str[0:2], "")
        
        # Check if there is a country code (must be exactly two uppercase letters)
        if length >= 5 and locale_str[3].isupper() and locale_str[4].isupper():
            # We have a country code
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
        else:
            # No country code, variant may start immediately after the underscore
            if length == 3:
                return Locale(locale_str[0:2], "")
            # There is at least one character after the underscore
            if locale_str[3] == '_':
                # Empty country, variant starts at position 4
                return Locale(locale_str[0:2], "", locale_str[4:])
            else:
                # Variant starts immediately after the underscore (no country)
                return Locale(locale_str[0:2], "", locale_str[3:])