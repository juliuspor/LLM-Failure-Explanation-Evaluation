    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length == 2:
            # Validate two lowercase letters
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")
        
        # For lengths other than 2, we need at least 5 characters (e.g., en_US)
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # First two characters must be lowercase letters
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Third character must be underscore
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Fourth and fifth characters must be uppercase letters
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if not ('A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        
        # For longer strings, we need at least 7 characters (e.g., en_US_xxx)
        if length < 7:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Sixth character must be underscore
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # The rest is the variant
        return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])