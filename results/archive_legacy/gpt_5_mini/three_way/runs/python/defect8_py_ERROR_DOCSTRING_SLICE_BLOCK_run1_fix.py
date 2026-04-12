@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        parts = locale_str.split('_', 2)
        if len(parts) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = parts[0]
        if len(language) != 2 or not language.islower() or not language.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        if len(parts) == 1:
            return Locale(language, "", "")
        if len(parts) == 2:
            country_part = parts[1]
            if country_part == "":
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(country_part) != 2 or not country_part.isupper() or not country_part.isalpha():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country_part, "")
        country_part = parts[1]
        variant = parts[2]
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        if country_part == "":
            return Locale(language, "", variant)
        if len(country_part) != 2 or not country_part.isupper() or not country_part.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country_part, variant)