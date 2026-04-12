@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        parts = locale_str.split('_', 2)
        if len(parts[0]) != 2 or not parts[0].islower() or not parts[0].isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = parts[0]
        country = ""
        variant = ""
        if len(parts) >= 2:
            country = parts[1]
        if len(parts) == 3:
            variant = parts[2]
        if country:
            if len(country) != 2 or not country.isupper() or not country.isalpha():
                raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country, variant)