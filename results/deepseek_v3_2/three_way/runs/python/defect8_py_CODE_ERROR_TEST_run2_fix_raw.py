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
        
        # At least 3 characters, check for underscore at position 2
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 3:
            # Only language and underscore (empty country, no variant)
            return Locale(locale_str[0:2], "")
        
        # length >= 4
        # Check if there is a country code (two uppercase letters) or empty country (another underscore)
        if length >= 5 and locale_str[3] != '_':
            # There is a country code at positions 3 and 4
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                # length >= 6
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                # variant starts at position 6
                return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
        else:
            # Empty country: next character is underscore at position 3
            # So we have language, underscore, underscore, variant
            if length == 4:
                # Only language and double underscore, no variant? Actually format would be "fr__" which is invalid because variant missing.
                # But we can treat as empty country and empty variant? According to Java Locale, "fr__" is invalid.
                # We'll raise error.
                raise ValueError(f"Invalid locale format: {locale_str}")
            # Check that position 3 is '_' (already implied) and there is variant after second underscore
            if locale_str[3] != '_':
                # This case should not happen because we are in else branch where locale_str[3] != '_' is false.
                # But for safety:
                raise ValueError(f"Invalid locale format: {locale_str}")
            # variant starts at position 4
            return Locale(locale_str[0:2], "", locale_str[4:])