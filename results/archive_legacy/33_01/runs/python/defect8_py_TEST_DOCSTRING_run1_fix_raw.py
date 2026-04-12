@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        if length == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if '_' not in locale_str:
            if length != 2:
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")
        parts = locale_str.split('_', 2)
        language = parts[0]
        country = ""
        variant = ""
        if len(parts) >= 2:
            country = parts[1]
        if len(parts) == 3:
            variant = parts[2]
        if len(language) != 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = language[0]
        ch1 = language[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if country:
            if len(country) != 2:
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch3 = country[0]
            ch4 = country[1]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
        if variant and not country and locale_str.find('__') == -1:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country, variant)