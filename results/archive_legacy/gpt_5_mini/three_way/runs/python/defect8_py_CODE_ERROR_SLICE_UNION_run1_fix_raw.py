@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    parts = locale_str.split('_', 2)
    if len(parts) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")
    lang = parts[0]
    if len(lang) != 2 or not (lang[0].islower() and lang[1].islower()):
        raise ValueError(f"Invalid locale format: {locale_str}")
    if len(parts) == 1:
        return Locale(lang, "")
    if len(parts) == 2:
        country = parts[1]
        if country == "":
            return Locale(lang, "")
        if len(country) != 2 or not (country[0].isupper() and country[1].isupper()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, country)
    country = parts[1]
    variant = parts[2]
    if country == "":
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, "", variant)
    if len(country) != 2 or not (country[0].isupper() and country[1].isupper()):
        raise ValueError(f"Invalid locale format: {locale_str}")
    if variant == "":
        raise ValueError(f"Invalid locale format: {locale_str}")
    return Locale(lang, country, variant)