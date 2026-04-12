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
            # language + underscore only (e.g., "en_") - treat as language only
            return Locale(locale_str[0:2], "")
        
        if length >= 5 and locale_str[3] == '_':
            # language + underscore + underscore (e.g., "fr__POSIX") -> empty country
            country = ""
            variant = locale_str[4:] if length > 4 else ""
            return Locale(locale_str[0:2], country, variant)
        
        if length >= 5:
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
        
        # length is 4 (e.g., "en_A") - invalid because country code must be two letters
        raise ValueError(f"Invalid locale format: {locale_str}")