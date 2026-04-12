    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        # Remove any leading/trailing whitespace (common in user input)
        locale_str = locale_str.strip()
        length = len(locale_str)
        
        # Language must be at least 2 characters
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
        
        # Must have at least one separator after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If length is 3, that's just language + underscore (invalid, but handle gracefully?)
        if length == 3:
            # Could be language + underscore with empty country and variant? Not standard.
            # We'll treat as language only, but spec says invalid. We'll raise error.
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Now we have at least 4 characters: xx_?
        # Check if the next part is country (2 uppercase letters) or empty country (another underscore)
        if length >= 5 and locale_str[3] == '_':
            # Double underscore: language__variant
            # Country is empty, variant starts after the second underscore
            if length < 7:  # Need at least xx__v (5 chars) but variant must be at least 1 char after __
                # Actually, xx__ is invalid because variant is empty.
                raise ValueError(f"Invalid locale format: {locale_str}")
            # Ensure there is at least one character after the double underscore
            variant_start = 4  # index after second underscore
            variant = locale_str[variant_start:]
            return Locale(locale_str[0:2], "", variant)
        else:
            # Normal case: language_country or language_country_variant
            # Validate country code (2 uppercase letters)
            if length < 5:
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
                if length == 6:
                    # xx_YY_ (variant empty) invalid
                    raise ValueError(f"Invalid locale format: {locale_str}")
                variant = locale_str[6:]
                return Locale(locale_str[0:2], locale_str[3:5], variant)