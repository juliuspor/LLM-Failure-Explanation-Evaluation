@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    length = len(locale_str)
    if length != 2 and length != 5 and length < 7:
        raise ValueError(f"Invalid locale format: {locale_str}")
    parts = locale_str.split('_')
    language = parts[0]
    if len(language) != 2 or not language.isalpha() or not language.islower():
        raise ValueError(f"Invalid locale format: {locale_str}")
    if len(parts) == 1:
        return Locale(language, "")
    if len(parts) == 2:
        country = parts[1]
        if country == "":
            return Locale(language, "")
        if len(country) != 2 or not country.isalpha() or not country.isupper():
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country)
    country = parts[1]
    variant = "_".join(parts[2:])
    if country == "":
        return Locale(language, "", variant)
    if len(country) != 2 or not country.isalpha() or not country.isupper():
        raise ValueError(f"Invalid locale format: {locale_str}")
    return Locale(language, country, variant)