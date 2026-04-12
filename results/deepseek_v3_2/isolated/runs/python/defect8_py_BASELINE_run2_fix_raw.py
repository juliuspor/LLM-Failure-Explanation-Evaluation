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
                # Only language and underscore, no country or variant
                return Locale(locale_str[0:2], "")
            
            # Check if there is a country code (two uppercase letters) or empty country
            if length >= 5 and locale_str[3] != '_' and locale_str[4] != '_':
                # Has a country code
                ch3 = locale_str[3]
                ch4 = locale_str[4]
                if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                
                if length == 5:
                    return Locale(locale_str[0:2], locale_str[3:5])
                else:
                    if locale_str[5] != '_':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
            else:
                # Empty country code (second underscore at position 3)
                # locale_str[3] is '_'
                if length == 4:
                    # Only language and double underscore, no variant
                    return Locale(locale_str[0:2], "")
                else:
                    # There is a variant after the second underscore
                    if locale_str[3] != '_':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    return Locale(locale_str[0:2], "", locale_str[4:])