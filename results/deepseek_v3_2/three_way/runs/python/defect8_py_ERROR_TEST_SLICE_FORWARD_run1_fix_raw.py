    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate first two characters as lowercase letters
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Language only (e.g., "en")
        if length == 2:
            return Locale(locale_str, "")
        
        # Must have at least 3 characters and underscore at position 2
        if length < 3 or locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Language with country and possibly variant (e.g., "en_US" or "en_US_VARIANT")
        if length == 5:
            # Exactly 5 chars: language (2) + '_' + country (2)
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5])
        
        # Handle longer strings: could be language + country + variant OR language + empty country + variant
        if length >= 6:
            # Check if country part is empty (two underscores after language)
            if locale_str[3] == '_':
                # Format: language + "__" + variant (e.g., "fr__POSIX")
                # Country is empty, variant starts at index 4
                if length < 4:
                    raise ValueError(f"Invalid locale format: {locale_str}")
                variant = locale_str[4:] if length > 4 else ""
                return Locale(locale_str[0:2], "", variant)
            else:
                # Format: language + "_" + country + "_" + variant (e.g., "en_US_VARIANT")
                # Validate country (positions 3 and 4) as uppercase letters
                if length < 5:
                    raise ValueError(f"Invalid locale format: {locale_str}")
                ch3 = locale_str[3]
                ch4 = locale_str[4]
                if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                # Ensure there is an underscore after country
                if length < 6 or locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                variant = locale_str[6:] if length > 6 else ""
                return Locale(locale_str[0:2], locale_str[3:5], variant)
        
        # If none of the above, it's invalid
        raise ValueError(f"Invalid locale format: {locale_str}")