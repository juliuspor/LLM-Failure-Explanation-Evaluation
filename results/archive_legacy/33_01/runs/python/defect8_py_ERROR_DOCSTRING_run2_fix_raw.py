@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    parts = locale_str.split('_', 2)
    if len(parts) == 1:
        lang = parts[0]
        if len(lang) != 2 or not lang.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, "")
    if len(parts) == 2:
        lang, country = parts[0], parts[1]
        if len(lang) != 2 or not lang.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        if len(country) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if len(country) == 2 and country.isupper():
            return Locale(lang, country)
        raise ValueError(f"Invalid locale format: {locale_str}")
    lang, country, variant = parts[0], parts[1], parts[2]
    if len(lang) != 2 or not lang.islower():
        raise ValueError(f"Invalid locale format: {locale_str}")
    if len(country) == 0:
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, "", variant)
    if len(country) == 2 and country.isupper():
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, country, variant)
    raise ValueError(f"Invalid locale format: {locale_str}")