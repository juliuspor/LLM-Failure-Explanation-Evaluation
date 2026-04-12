@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        if locale_str == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        if '-' in locale_str:
            raise ValueError(f"Invalid locale format: {locale_str}")
        parts = locale_str.split('_')
        if len(parts) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = parts[0]
        if not (len(language) == 2 and language.isalpha() and language.islower()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = ""
        variant = ""
        if len(parts) >= 2 and parts[1] != "":
            country = parts[1]
            if not (len(country) == 2 and country.isalpha() and country.isupper()):
                raise ValueError(f"Invalid locale format: {locale_str}")
        if len(parts) >= 3:
            variant = "_".join(parts[2:])
        return Locale(language, country, variant)