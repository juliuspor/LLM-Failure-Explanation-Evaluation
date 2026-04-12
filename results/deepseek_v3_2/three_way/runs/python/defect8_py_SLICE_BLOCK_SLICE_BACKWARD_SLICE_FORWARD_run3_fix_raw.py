    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        """
        Parse a locale string into a Locale object.
        """
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate first two characters are lowercase letters
        if length >= 2:
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 2:
            return Locale(locale_str, "")
        
        # For longer strings, we need at least 5 characters (ll_CC) or 6+ (ll_CC_VV)
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check underscore at position 2
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate characters 3 and 4 are uppercase letters
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        
        # For length >= 6, we need underscore at position 5
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])