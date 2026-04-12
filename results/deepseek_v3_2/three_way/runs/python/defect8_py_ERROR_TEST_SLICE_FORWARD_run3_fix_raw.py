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
        
        # If length is 2, it's just language
        if length == 2:
            return Locale(locale_str, "")
        
        # Must have at least one underscore after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If length is 3, it's language + underscore only (invalid? but we'll treat as language only?)
        # Actually, length 3 would be like "en_", which is invalid. We'll raise.
        if length == 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Now we have at least 4 characters: "en_" + something
        # Check if the next character is another underscore (empty country)
        if locale_str[3] == '_':
            # Empty country, variant starts after the double underscore
            # Language is locale_str[0:2]
            # Country is empty
            # Variant is everything after the double underscore (position 4 onwards)
            if length == 4:
                # Only double underscore, no variant: e.g., "en__"
                return Locale(locale_str[0:2], "", "")
            else:
                variant = locale_str[4:]
                return Locale(locale_str[0:2], "", variant)
        else:
            # We have a country code (uppercase letters) at positions 3 and 4
            if length == 4:
                # Only one character after underscore? Should be two for country.
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                # Variant starts at position 6
                variant = locale_str[6:] if length > 6 else ""
                return Locale(locale_str[0:2], locale_str[3:5], variant)