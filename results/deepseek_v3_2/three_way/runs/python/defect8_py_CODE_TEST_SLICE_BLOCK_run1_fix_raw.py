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
        
        # length >= 3 and has underscore at position 2
        if length == 3:
            # only language and underscore, e.g., "en_"? treat as language only? but spec says invalid.
            # According to Java Locale, "en_" is invalid. We'll raise error.
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check if the next character is another underscore (empty country)
        if locale_str[3] == '_':
            # format: language__variant
            if length < 5:
                # need at least language + "__" + variant (min 1 char) => length >= 5
                raise ValueError(f"Invalid locale format: {locale_str}")
            # country is empty, variant starts at position 4 (since 3 is underscore)
            variant = locale_str[4:] if length > 4 else ""
            return Locale(locale_str[0:2], "", variant)
        
        # Otherwise, we have a country code (must be two uppercase letters)
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
            variant = locale_str[6:] if length > 6 else ""
            return Locale(locale_str[0:2], locale_str[3:5], variant)