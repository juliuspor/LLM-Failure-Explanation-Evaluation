@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    parts = locale_str.split('_')
    if len(parts) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")
    language = parts[0]
    if len(language) != 2 or not language.islower():
        raise ValueError(f"Invalid locale format: {locale_str}")
    country = ""
    variant = ""
    if len(parts) == 1:
        return Locale(language, "", "")
    if len(parts) == 2:
        country_part = parts[1]
        if country_part:
            if len(country_part) != 2 or not country_part.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
            country = country_part
        return Locale(language, country, "")
    if len(parts) >= 3:
        country_part = parts[1]
        variant_part = "_".join(parts[2:])
        if country_part:
            if len(country_part) != 2 or not country_part.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
            country = country_part
        if not variant_part:
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = variant_part
        return Locale(language, country, variant)