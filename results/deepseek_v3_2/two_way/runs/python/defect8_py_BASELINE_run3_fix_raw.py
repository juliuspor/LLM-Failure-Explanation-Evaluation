    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate first two characters are lowercase letters
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 2:
            return Locale(locale_str, "")
        
        # Must have at least 3 characters to have a separator
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Now we have at least "xx_"
        if length == 3:
            # Only language and underscore (empty country/variant) -> treat as language only
            return Locale(locale_str[0:2], "")
        
        # Check if the next character is another underscore (empty country)
        if locale_str[3] == '_':
            # Format: xx__variant
            # Country is empty, variant starts after the double underscore
            if length == 4:
                # Only "xx__" -> variant is empty? treat as language only
                return Locale(locale_str[0:2], "")
            # variant is from position 4 to end
            return Locale(locale_str[0:2], "", locale_str[4:])
        
        # Otherwise, we expect a two-letter uppercase country code
        if length < 5:
            # Need at least 5 characters for "xx_YY"
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        
        # Check for variant separator
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # variant is from position 6 to end
        return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])