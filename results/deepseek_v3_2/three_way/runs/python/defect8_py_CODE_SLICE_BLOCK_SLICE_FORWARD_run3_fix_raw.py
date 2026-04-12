    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        # Valid lengths: 2 (language only), 5 (language_country), >=7 (language_country_variant)
        # Length 6 is invalid because it would be language_country_ with empty variant (6 chars) but that's not a standard format.
        # However, the original check incorrectly rejected length 6 even if it could be parsed.
        # We'll adjust the condition to allow length 6 as well, but we must ensure proper parsing.
        # Actually, the standard format expects language (2) + '_' + country (2) = 5, or with variant at least 7.
        # A length of 6 would be language (2) + '_' + country (2) + '_' + (variant length 1) = 6, which is valid.
        # So we need to allow length >=5 and handle the cases appropriately.
        # Let's refactor: check basic length and structure.
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate first two characters are lowercase letters
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 2:
            return Locale(locale_str, "")
        
        # At least 5 characters for language_country
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check for underscore after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate country code (two uppercase letters)
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        else:
            # Length >=6, must have second underscore at position 5
            if locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            # Variant is everything after the second underscore
            return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])