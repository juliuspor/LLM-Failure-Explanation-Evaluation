    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        # Valid lengths: 2 (language only), 5 (language_country), or >=7 (language_country_variant)
        if length != 2 and length != 5 and length < 7:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate first two characters are lowercase letters
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 2:
            return Locale(locale_str, "")
        else:
            # Must have underscore at position 2
            if locale_str[2] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            # Validate country code (positions 3 and 4) are uppercase letters
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                # Must have underscore at position 5
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                # Variant is everything after position 5
                variant = locale_str[6:]
                # Ensure variant is non-empty (optional, but original code allowed empty variant?)
                # The Locale constructor accepts empty variant, so we can allow it.
                return Locale(locale_str[0:2], locale_str[3:5], variant)