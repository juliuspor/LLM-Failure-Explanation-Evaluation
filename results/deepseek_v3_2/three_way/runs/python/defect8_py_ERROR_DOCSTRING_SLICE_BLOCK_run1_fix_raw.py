    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        if not locale_str:
            raise ValueError(f"Invalid locale format: {locale_str}")
        parts = locale_str.split('_')
        if len(parts) == 1:
            language = parts[0]
            if len(language) != 2 or not language.isalpha() or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, "")
        elif len(parts) == 2:
            language, country = parts
            if len(language) != 2 or not language.isalpha() or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if country:
                if len(country) != 2 or not country.isalpha() or not country.isupper():
                    raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country)
        elif len(parts) == 3:
            language, country, variant = parts
            if len(language) != 2 or not language.isalpha() or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if country:
                if len(country) != 2 or not country.isalpha() or not country.isupper():
                    raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country, variant)
        else:
            raise ValueError(f"Invalid locale format: {locale_str}")