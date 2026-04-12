    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length == 2:
            # Two characters must be lowercase letters
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")
        
        # For lengths >= 5, we need at least 5 characters and an underscore at position 2
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check first two characters are lowercase letters
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check country code (positions 3 and 4) are uppercase letters
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        else:
            # Length >= 6, must have another underscore at position 5
            if locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            # Variant is everything after the second underscore
            return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])