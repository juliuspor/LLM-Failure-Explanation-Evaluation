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
        else:
            if locale_str[2] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            
            if length == 3:
                raise ValueError(f"Invalid locale format: {locale_str}")
            
            ch3 = locale_str[3]
            if ch3 == '_':
                # Format: language__variant (empty country)
                if length == 4:
                    # Only language and double underscore, no variant (e.g., "fr__")
                    return Locale(locale_str[0:2], "", "")
                else:
                    # language__variant (e.g., "fr__POSIX")
                    return Locale(locale_str[0:2], "", locale_str[4:])
            else:
                # Format: language_country or language_country_variant
                if length == 3 or length == 4:
                    raise ValueError(f"Invalid locale format: {locale_str}")
                
                if length == 5:
                    ch4 = locale_str[4]
                    if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    return Locale(locale_str[0:2], locale_str[3:5])
                else:
                    if length < 7:
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    
                    ch4 = locale_str[4]
                    if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    
                    if locale_str[5] != '_':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    
                    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])