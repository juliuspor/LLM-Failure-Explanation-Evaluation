@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    parts = locale_str.split('_', 2)
    if len(parts) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")
    language = parts[0]
    if len(language) != 2 or language[0] < 'a' or language[0] > 'z' or language[1] < 'a' or language[1] > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")
    if len(parts) == 1:
        return Locale(language, "")
    country = parts[1]
    variant = ""
    if len(parts) == 3:
        variant = parts[2]
    if country == "":
        if variant == "":
            return Locale(language, "")
        return Locale(language, "", variant)
    if len(country) != 2 or country[0] < 'A' or country[0] > 'Z' or country[1] < 'A' or country[1] > 'Z':
        raise ValueError(f"Invalid locale format: {locale_str}")
    if variant == "":
        return Locale(language, country)
    return Locale(language, country, variant)