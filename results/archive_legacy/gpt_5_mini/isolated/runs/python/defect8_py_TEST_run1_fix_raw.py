@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    parts = locale_str.split('_', 2)
    if len(parts) == 0 or parts[0] == "":
        raise ValueError(f"Invalid locale format: {locale_str}")
    language = parts[0]
    if len(language) != 2 or not language.isalpha() or language != language.lower():
        raise ValueError(f"Invalid locale format: {locale_str}")
    country = ""
    variant = ""
    if len(parts) >= 2:
        country = parts[1]
        if country != "" and (len(country) != 2 or not country.isalpha() or country != country.upper()):
            raise ValueError(f"Invalid locale format: {locale_str}")
    if len(parts) == 3:
        variant = parts[2]
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
    return Locale(language, country, variant)