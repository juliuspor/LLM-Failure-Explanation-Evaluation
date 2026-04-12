    @classmethod
    def to_locale(cls, locale_str: str) -> Locale:
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
            # Only language and underscore (e.g., "fr_")
            return Locale(locale_str[0:2], "")
        
        # Check for empty country (double underscore)
        if locale_str[3] == '_':
            # Format: language__variant
            country = ""
            variant_start = 4
        else:
            # Expect a two-letter uppercase country code
            if length < 5:
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            country = locale_str[3:5]
            variant_start = 5
            if length > variant_start and locale_str[variant_start] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if length > variant_start:
                variant_start += 1  # skip the underscore
        
        variant = ""
        if length > variant_start:
            variant = locale_str[variant_start:]
        
        return Locale(locale_str[0:2], country, variant)