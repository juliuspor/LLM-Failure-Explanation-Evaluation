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
        
        # At least 3 characters, check for underscore
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 3:
            # Only language and underscore, e.g., "fr_" (though unusual)
            return Locale(locale_str[0:2], "")
        
        # Now we have at least 4 characters: "fr_X..."
        # Check if the next character is another underscore (empty country)
        if locale_str[3] == '_':
            # Empty country, e.g., "fr__POSIX"
            # Country is empty, variant starts after the second underscore
            if length == 4:
                # Only "fr__" (no variant) -> treat as language only
                return Locale(locale_str[0:2], "")
            # variant starts at position 4 (after second underscore)
            return Locale(locale_str[0:2], "", locale_str[4:])
        
        # We have a country code (must be two uppercase letters)
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        
        # Check for third underscore before variant
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 6:
            # Only language, country, and trailing underscore (no variant)
            return Locale(locale_str[0:2], locale_str[3:5])
        
        # Variant present
        return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])