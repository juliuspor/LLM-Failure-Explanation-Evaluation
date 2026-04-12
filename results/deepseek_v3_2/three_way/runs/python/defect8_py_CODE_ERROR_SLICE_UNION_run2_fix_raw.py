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
        
        ch3 = locale_str[3]
        if ch3 == '_':
            # Double underscore indicates empty country (e.g., "fr__POSIX")
            country = ""
            variant_start = 4
        else:
            # Normal case: country code expected
            if length < 5:
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            country = locale_str[3:5]
            variant_start = 5
            if length > 5 and locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant_start = 6  # skip underscore after country
        
        if length > variant_start:
            variant = locale_str[variant_start:]
        else:
            variant = ""
        
        return Locale(locale_str[0:2], country, variant)