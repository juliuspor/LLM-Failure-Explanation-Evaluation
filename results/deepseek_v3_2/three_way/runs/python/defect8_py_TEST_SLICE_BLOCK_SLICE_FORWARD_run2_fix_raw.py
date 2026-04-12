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
        
        # If length is 2, just language
        if length == 2:
            return Locale(locale_str, "")
        
        # Must have at least 3 characters for separator
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If length is 3, that's just language_ (invalid)
        if length == 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Now we have at least 4 characters: xx_?
        # Check if the next character is '_' (empty country) or uppercase letter
        ch3 = locale_str[3]
        if ch3 == '_':
            # Empty country: format is xx__variant
            if length == 4:
                # Only xx__ (invalid, missing variant)
                raise ValueError(f"Invalid locale format: {locale_str}")
            # variant starts at index 4
            variant = locale_str[4:] if length > 4 else ""
            return Locale(locale_str[0:2], "", variant)
        else:
            # Expect a country code: two uppercase letters
            if length < 5:
                raise ValueError(f"Invalid locale format: {locale_str}")
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