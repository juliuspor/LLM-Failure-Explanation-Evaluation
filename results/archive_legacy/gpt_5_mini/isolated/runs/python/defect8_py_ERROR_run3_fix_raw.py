@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    if len(locale_str) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")
    parts = locale_str.split('_', 2)
    language = parts[0]
    if len(language) < 1 or any(c < 'a' or c > 'z' for c in language):
        raise ValueError(f"Invalid locale format: {locale_str}")
    if len(parts) == 1:
        return Locale(language, "")
    country = parts[1]
    if country != "" and (len(country) != 2 or any(c < 'A' or c > 'Z' for c in country)):
        raise ValueError(f"Invalid locale format: {locale_str}")
    if len(parts) == 2:
        return Locale(language, country)
    variant = parts[2]
    if variant == "":
        raise ValueError(f"Invalid locale format: {locale_str}")
    return Locale(language, country, variant)