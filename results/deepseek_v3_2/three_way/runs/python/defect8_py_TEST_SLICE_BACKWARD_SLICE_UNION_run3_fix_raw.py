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
        
        # If length is 2, only language
        if length == 2:
            return Locale(locale_str, "")
        
        # Must have at least one underscore after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If length is 3, only language and underscore (invalid? but we'll treat as language only?)
        # Actually, length 3 would be like "en_", which is invalid. We'll raise.
        if length == 3:
            # Only language and underscore, no country or variant
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Now we have at least 4 characters: "en_A" or "en__"
        ch3 = locale_str[3]
        
        # Check if the third character is an uppercase letter -> country code
        if ch3 >= 'A' and ch3 <= 'Z':
            # We have a country code, need at least one more character for country (2 letters)
            if length < 5:
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch4 = locale_str[4]
            if ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            # Now we have language_country (5 chars) or language_country_variant
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                # variant starts at position 6
                return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
        else:
            # Third character is not uppercase, so it must be '_' for double underscore
            if ch3 != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            # Double underscore case: language__variant
            # Country is empty, variant starts at position 4
            # But we need to ensure there is at least a variant character after the double underscore
            if length < 5:
                # Something like "fr__" (length 4) is invalid because no variant after double underscore
                raise ValueError(f"Invalid locale format: {locale_str}")
            # variant starts at position 4 (since we have language, underscore, underscore, variant)
            return Locale(locale_str[0:2], "", locale_str[4:])