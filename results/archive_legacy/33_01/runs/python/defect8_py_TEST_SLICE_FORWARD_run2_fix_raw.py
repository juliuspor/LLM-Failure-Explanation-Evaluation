@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    parts = locale_str.split('_', 2)
    if len(parts) == 1:
        language = parts[0]
        if len(language) != 2 or not language.islower() or not language.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, "")
    language = parts[0]
    if len(language) != 2 or not language.islower() or not language.isalpha():
        raise ValueError(f"Invalid locale format: {locale_str}")
    country = parts[1]
    variant = ""
    if len(parts) == 3:
        variant = parts[2]
    if country == "":
        return Locale(language, "", variant)
    if len(country) != 2 or not country.isupper() or not country.isalpha():
        raise ValueError(f"Invalid locale format: {locale_str}")
    return Locale(language, country, variant)