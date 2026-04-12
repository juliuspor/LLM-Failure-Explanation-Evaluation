@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        # Accept lengths: 2 (language), 5 (language_country), or >=7 (language_country_variant)
        if not (length == 2 or length == 5 or length >= 7):
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
            
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            # Allow either two uppercase letters for country or two underscores indicating empty country
            is_country_chars = (ch3 >= 'A' and ch3 <= 'Z' and ch4 >= 'A' and ch4 <= 'Z')
            is_empty_country = (ch3 == '_' and ch4 == '_')
            if not (is_country_chars or is_empty_country):
                raise ValueError(f"Invalid locale format: {locale_str}")
            
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                # Variant case: handle empty country ("__") or normal country followed by '_' then variant
                if is_empty_country:
                    if locale_str[5] != '_':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    return Locale(locale_str[0:2], "", locale_str[6:])
                else:
                    if locale_str[5] != '_':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])