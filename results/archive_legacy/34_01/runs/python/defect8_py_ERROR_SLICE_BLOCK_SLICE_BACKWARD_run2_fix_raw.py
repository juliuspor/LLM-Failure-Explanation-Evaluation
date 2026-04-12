@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        parts = locale_str.split('_', 2)
        language = parts[0]
        if len(language) != 2 or not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        if len(parts) == 1:
            return Locale(language, "")
        country = parts[1]
        if country == "":
            if len(parts) == 2:
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = parts[2]
            if variant == "":
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, "", variant)
        else:
            if len(country) != 2 or not country.isalpha() or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(parts) == 2:
                return Locale(language, country)
            variant = parts[2]
            if variant == "":
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country, variant)