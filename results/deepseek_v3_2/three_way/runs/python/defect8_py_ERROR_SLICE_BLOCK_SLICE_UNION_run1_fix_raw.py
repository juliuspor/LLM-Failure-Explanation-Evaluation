    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 2:
            return Locale(locale_str, "")
        
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 3:
            # Only language and underscore, e.g., "en_"? Not valid.
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Now we have at least 4 characters: xx_?
        # Check if there's a country code (two uppercase letters) after underscore
        if length >= 5:
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if 'A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z':
                # We have a country code
                country = locale_str[3:5]
                if length == 5:
                    return Locale(locale_str[0:2], country)
                else:
                    if locale_str[5] != '_':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    variant = locale_str[6:] if length > 6 else ""
                    return Locale(locale_str[0:2], country, variant)
            else:
                # No country code, treat the part after underscore as variant
                # But note: the underscore at position 2 is already consumed.
                # So variant starts at index 3.
                variant = locale_str[3:] if length > 3 else ""
                return Locale(locale_str[0:2], "", variant)
        else:
            # length is 4: xx_? (single character after underscore)
            # That single character could be part of variant, but standard expects
            # either country (2 letters) or variant (any). However, we can treat it as variant.
            variant = locale_str[3:] if length > 3 else ""
            return Locale(locale_str[0:2], "", variant)