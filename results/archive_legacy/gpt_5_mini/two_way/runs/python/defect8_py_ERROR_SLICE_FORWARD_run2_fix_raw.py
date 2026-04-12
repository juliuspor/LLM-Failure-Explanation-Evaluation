@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    parts = locale_str.split('_', 2)
    if len(parts) == 1:
        lang = parts[0]
        if len(lang) != 2 or not lang.islower() or not lang.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, "")
    elif len(parts) == 2:
        lang, country = parts
        if len(lang) != 2 or not lang.islower() or not lang.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        if country == "":
            return Locale(lang, "")
        if len(country) != 2 or not country.isupper() or not country.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, country)
    else:
        lang, country, variant = parts
        if len(lang) != 2 or not lang.islower() or not lang.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        if country == "":
            return Locale(lang, "", variant)
        if len(country) != 2 or not country.isupper() or not country.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, country, variant)