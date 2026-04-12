@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    length = len(locale_str)
    if length != 2 and length != 5 and length < 7:
        raise ValueError(f"Invalid locale format: {locale_str}")
    if length >= 2:
        language = locale_str[0:2]
        if not language.isalpha() or len(language) != 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
    else:
        raise ValueError(f"Invalid locale format: {locale_str}")
    if length == 2:
        return Locale(language.lower(), "")
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    country = locale_str[3:5]
    if not country.isalpha() or len(country) != 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    if length == 5:
        return Locale(language.lower(), country.upper())
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    variant = locale_str[6:]
    return Locale(language.lower(), country.upper(), variant)