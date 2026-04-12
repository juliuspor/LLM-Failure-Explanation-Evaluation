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
        
        # Must have at least one underscore after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If length is 3, only language and underscore (invalid? but handle)
        if length == 3:
            # Only language and underscore, treat as language only
            return Locale(locale_str[0:2], "")
        
        # Now length >= 4
        # Check if there is a country (uppercase letters) or another underscore (empty country)
        ch3 = locale_str[3]
        if ch3 == '_':
            # Empty country, variant starts at index 4
            # Language is locale_str[0:2], country is "", variant is locale_str[4:]
            return Locale(locale_str[0:2], "", locale_str[4:])
        else:
            # Expect country code of two uppercase letters
            if length < 5:
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            
            # Now we have language and country
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                # Must have underscore before variant
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])