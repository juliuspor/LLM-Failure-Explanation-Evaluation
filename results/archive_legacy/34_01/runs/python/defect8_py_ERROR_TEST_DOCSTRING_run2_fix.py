@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        parts = locale_str.split('_')
        if len(parts) == 1:
            lang = parts[0]
            if len(lang) != 2 or not lang.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang, "")
        elif len(parts) == 2:
            lang, country = parts
            if len(lang) != 2 or not lang.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(country) != 2 or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang, country)
        elif len(parts) == 3:
            lang, country, variant = parts
            if len(lang) != 2 or not lang.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if country != "" and (len(country) != 2 or not country.isupper()):
                raise ValueError(f"Invalid locale format: {locale_str}")
            if variant is None or len(variant) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang, country, variant)
        else:
            raise ValueError(f"Invalid locale format: {locale_str}")