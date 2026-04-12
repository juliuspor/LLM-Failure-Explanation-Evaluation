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
                # Only language and underscore (e.g., "en_")? Not valid.
                raise ValueError(f"Invalid locale format: {locale_str}")
            
            # Check if country code is present (two uppercase letters) or empty (next char is '_')
            if length >= 5 and locale_str[3] != '_' and locale_str[4] != '_':
                ch3 = locale_str[3]
                ch4 = locale_str[4]
                if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                country = locale_str[3:5]
                variant_start = 5
            else:
                # Empty country code
                country = ""
                variant_start = 3
            
            # Now handle variant if any
            if length > variant_start:
                if locale_str[variant_start] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                variant = locale_str[variant_start+1:]
            else:
                variant = ""
            
            return Locale(locale_str[0:2], country, variant)