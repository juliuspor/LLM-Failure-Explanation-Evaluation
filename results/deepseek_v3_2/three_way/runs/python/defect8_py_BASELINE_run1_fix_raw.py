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
        
        # If length is 3, that's just language_ (invalid? but we'll treat as language only?)
        # Actually, length 3 would be e.g., "en_", which is invalid. We'll raise.
        if length == 3:
            # Only language and underscore, no country or variant
            # According to Java Locale, this is invalid. So raise.
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Now we have at least 4 characters: language + '_' + something
        # Check if the next character is another underscore (empty country)
        if locale_str[3] == '_':
            # Empty country, variant follows after second underscore
            # language__variant
            # variant starts at index 4
            if length == 4:
                # Only language and double underscore, no variant: e.g., "fr__"
                # This is invalid because variant is empty.
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = locale_str[4:]
            # Validate variant? No restrictions on variant.
            return Locale(locale_str[0:2], "", variant)
        else:
            # Expect a country code (two uppercase letters)
            if length < 5:
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            
            if length == 5:
                # language_COUNTRY
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                # Must have another underscore before variant
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                if length == 6:
                    # language_COUNTRY_ (no variant) -> invalid
                    raise ValueError(f"Invalid locale format: {locale_str}")
                variant = locale_str[6:]
                return Locale(locale_str[0:2], locale_str[3:5], variant)