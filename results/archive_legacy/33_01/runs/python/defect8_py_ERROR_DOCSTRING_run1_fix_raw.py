@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        parts = locale_str.split('_', 2)
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
        elif len(parts) == 3:
            language, country, variant = parts[0], parts[1], parts[2]
            if len(language) != 2 or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if country != "":
                if len(country) != 2 or not country.isupper():
                    raise ValueError(f"Invalid locale format: {locale_str}")
            if len(variant) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country, variant)
        else:
            raise ValueError(f"Invalid locale format: {locale_str}")