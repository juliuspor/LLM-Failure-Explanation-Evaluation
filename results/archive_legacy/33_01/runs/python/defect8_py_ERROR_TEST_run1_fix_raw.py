@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    parts = locale_str.split('_', 2)
    if len(parts[0]) != 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    lang0 = parts[0]
    if not ('a' <= lang0[0] <= 'z' and 'a' <= lang0[1] <= 'z'):
        raise ValueError(f"Invalid locale format: {locale_str}")
    if len(parts) == 1:
        return Locale(lang0, "", "")
    country = parts[1]
    if country != "" and len(country) != 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    if country != "" and not ('A' <= country[0] <= 'Z' and 'A' <= country[1] <= 'Z'):
        raise ValueError(f"Invalid locale format: {locale_str}")
    if len(parts) == 2:
        return Locale(lang0, country, "")
    variant = parts[2]
    if len(variant) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")
    return Locale(lang0, country, variant)