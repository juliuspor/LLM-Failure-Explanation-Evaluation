@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        if length == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 1 or length == 3 or length == 4:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length >= 2:
            lang = locale_str[0:2]
            if len(lang) != 2 or not (lang[0].islower() and lang[1].islower()):
                raise ValueError(f"Invalid locale format: {locale_str}")
            if length == 2:
                return Locale(lang, "")
            if locale_str[2] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            country = locale_str[3:5]
            if len(country) != 2 or not (country[0].isupper() and country[1].isupper()):
                raise ValueError(f"Invalid locale format: {locale_str}")
            if length == 5:
                return Locale(lang, country)
            if locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = locale_str[6:]
            return Locale(lang, country, variant)
        raise ValueError(f"Invalid locale format: {locale_str}")