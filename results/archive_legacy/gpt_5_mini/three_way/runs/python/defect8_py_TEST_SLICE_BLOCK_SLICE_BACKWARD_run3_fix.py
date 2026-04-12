@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        parts = locale_str.split('_', 2)
        if len(parts) == 1:
            lang = parts[0]
            if len(lang) != 2 or not lang.isalpha() or not lang.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang, "")
        lang = parts[0]
        if len(lang) != 2 or not lang.isalpha() or not lang.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        if len(parts) == 2:
            country = parts[1]
            if country == "":
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(country) != 2 or not country.isalpha() or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang, country)
        country = parts[1]
        variant = parts[2]
        if country == "":
            if variant == "":
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang, "", variant)
        if len(country) != 2 or not country.isalpha() or not country.isupper():
            raise ValueError(f"Invalid locale format: {locale_str}")
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, country, variant)