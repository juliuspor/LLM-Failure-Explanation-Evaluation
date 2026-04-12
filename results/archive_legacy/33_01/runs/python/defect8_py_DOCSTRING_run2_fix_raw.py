@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    s = locale_str.strip()
    if s == "":
        raise ValueError(f"Invalid locale format: {locale_str}")
    s = s.replace('-', '_')
    parts = s.split('_')
    if len(parts) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")
    language = parts[0]
    if language == "":
        raise ValueError(f"Invalid locale format: {locale_str}")
    if not language.isalpha() or len(language) < 2 or len(language) > 3:
        raise ValueError(f"Invalid locale format: {locale_str}")
    language = language.lower()
    country = ""
    variant = ""
    if len(parts) >= 2 and parts[1] != "":
        country = parts[1]
        if not country.isalpha() or (len(country) != 2 and len(country) != 3):
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = country.upper()
    if len(parts) >= 3:
        variant = "_".join(parts[2:])
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
    return Locale(language, country, variant)