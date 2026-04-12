@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        if not isinstance(locale_str, str):
            raise ValueError(f"Invalid locale format: {locale_str}")
        length = len(locale_str)
        if length == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        parts = locale_str.split('_')
        if len(parts) == 1:
            language = parts[0]
            if len(language) != 2 or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, "")
        elif len(parts) == 2:
            language, country = parts[0], parts[1]
            if len(language) != 2 or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(country) != 2 or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country)
        else:
            language, country = parts[0], parts[1]
            variant = '_'.join(parts[2:])
            if len(language) != 2 or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(country) != 2 or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(variant) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country, variant)