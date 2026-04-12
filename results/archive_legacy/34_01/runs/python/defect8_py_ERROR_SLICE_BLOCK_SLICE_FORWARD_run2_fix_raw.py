@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = locale_str[0:2]
        if not language.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = language.lower()
        if length == 2:
            return Locale(language, "")
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if locale_str[3] == '_':
            variant = locale_str[4:]
            if variant == "":
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, "", variant)
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = locale_str[3:5]
        if not country.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = country.upper()
        if length == 5:
            return Locale(language, country)
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[6:]
        return Locale(language, country, variant)