@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    if len(locale_str) < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    lang = locale_str[0:2]
    if not (len(lang) == 2 and lang.isalpha() and lang == lang.lower()):
        raise ValueError(f"Invalid locale format: {locale_str}")
    if len(locale_str) == 2:
        return Locale(lang, "")
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    if len(locale_str) == 3:
        raise ValueError(f"Invalid locale format: {locale_str}")
    if locale_str[3] == '_':
        variant = locale_str[4:]
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, "", variant)
    else:
        if len(locale_str) < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = locale_str[3:5]
        if not (len(country) == 2 and country.isalpha()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = country.upper()
        if len(locale_str) == 5:
            return Locale(lang, country)
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[6:]
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, country, variant)