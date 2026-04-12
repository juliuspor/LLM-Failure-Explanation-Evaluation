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
        else:
            if locale_str[2] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            
            if length == 3:
                # Only language and underscore (e.g., "en_")
                return Locale(locale_str[0:2], "")
            
            # Check if there is a country code (two uppercase letters) or empty country (next char is '_')
            if length >= 5 and locale_str[3] != '_' and locale_str[4] != '_':
                ch3 = locale_str[3]
                ch4 = locale_str[4]
                if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                country = locale_str[3:5]
                if length == 5:
                    return Locale(locale_str[0:2], country)
                else:
                    if locale_str[5] != '_':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    variant = locale_str[6:] if length > 6 else ""
                    return Locale(locale_str[0:2], country, variant)
            else:
                # No country code (empty country) -> variant starts after second underscore
                # locale_str format: ll_ _variant (two underscores)
                if length >= 4 and locale_str[3] == '_':
                    # variant starts at index 4
                    variant = locale_str[4:] if length > 4 else ""
                    return Locale(locale_str[0:2], "", variant)
                else:
                    # length is 3 (already handled) or 4 with second char not underscore?
                    # Actually, if length >=4 and locale_str[3] != '_', then it's malformed.
                    # But we already checked that locale_str[2] == '_'.
                    # If length == 4, then locale_str[3] is the only character after underscore.
                    # That character could be the start of a variant, but the pattern expects
                    # either a country code (two uppercase) or a second underscore.
                    # So we treat a single character after underscore as variant? Not standard.
                    # According to Java Locale, the format is language_country_variant, where
                    # country is optional but if present must be two uppercase letters.
                    # So we raise error.
                    raise ValueError(f"Invalid locale format: {locale_str}")