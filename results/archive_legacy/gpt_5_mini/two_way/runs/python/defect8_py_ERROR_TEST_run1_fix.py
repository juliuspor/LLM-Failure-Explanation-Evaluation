@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        parts = locale_str.split('_', 2)
        language = parts[0]
        if len(language) != 2 or not language.islower() or not language.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = ""
        variant = ""
        if len(parts) > 1:
            country = parts[1]
        if len(parts) > 2:
            variant = parts[2]
        if country != "" and (len(country) != 2 or not country.isupper() or not country.isalpha()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if variant == "":
            if country == "":
                return Locale(language, "")
            else:
                return Locale(language, country)
        return Locale(language, country, variant)