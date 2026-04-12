@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    parts = locale_str.split('_', 2)
    if len(parts) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")
    language = parts[0]
    if len(language) != 2 or not language.isalpha() or not language.islower():
        raise ValueError(f"Invalid locale format: {locale_str}")
    if len(parts) == 1:
        return Locale(language, "")
    country = parts[1]
    if len(parts) == 2:
        if len(country) == 0:
            return Locale(language, "")
        if len(country) != 2 or not country.isalpha() or not country.isupper():
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country)
    variant = parts[2]
    if len(country) != 0 and (len(country) != 2 or not country.isalpha() or not country.isupper()):
        raise ValueError(f"Invalid locale format: {locale_str}")
    return Locale(language, country, variant)