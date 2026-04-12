@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 2:
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = locale_str[0:2]
        remainder = locale_str[3:]
        if remainder == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        parts = remainder.split('_', 1)
        country = parts[0]
        variant = parts[1] if len(parts) > 1 else ""
        if len(language) != 2 or language[0] < 'a' or language[0] > 'z' or language[1] < 'a' or language[1] > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if country != "" and (len(country) != 2 or country[0] < 'A' or country[0] > 'Z' or country[1] < 'A' or country[1] > 'Z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if variant == "":
            if country == "":
                return Locale(language, "")
            return Locale(language, country)
        return Locale(language, country, variant)