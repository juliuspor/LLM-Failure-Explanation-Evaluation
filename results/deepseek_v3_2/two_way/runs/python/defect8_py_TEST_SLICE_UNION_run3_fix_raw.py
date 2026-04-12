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
        
        # If length is 3, that's just language_ (invalid, but we can treat as language only?)
        # Actually, according to Java Locale, a single underscore after language is invalid.
        # We'll raise an error for length 3.
        if length == 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Now we have at least 4 characters: xx_?
        # Check if the next character is an underscore (empty country) or uppercase letter.
        ch3 = locale_str[3]
        if ch3 == '_':
            # Empty country, variant follows after second underscore
            # Format: xx__variant
            if length < 5:
                # Must have at least xx__ (4 chars) but no variant, which is invalid.
                raise ValueError(f"Invalid locale format: {locale_str}")
            # Ensure there is a variant after the second underscore
            variant = locale_str[4:] if length > 4 else ""
            if not variant:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], "", variant)
        else:
            # Expect a two-letter uppercase country code
            if length < 5:
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            
            # Now we have xx_CC or xx_CC_variant
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                variant = locale_str[6:] if length > 6 else ""
                return Locale(locale_str[0:2], locale_str[3:5], variant)