@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    if len(locale_str) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")
    parts = locale_str.split('_', 2)
    language = parts[0]
    if not (1 < len(language) <= 3) or not language.isalpha() or not language.islower():
        raise ValueError(f"Invalid locale format: {locale_str}")
    country = ''
    variant = ''
    if len(parts) >= 2:
        country = parts[1]
    if len(parts) == 3:
        variant = parts[2]
    if country == '' and variant == '':
        return Locale(language, "", "")
    if country != '' and (len(country) != 2 or not country.isalpha() or not country.isupper()):
        raise ValueError(f"Invalid locale format: {locale_str}")
    return Locale(language, country, variant)