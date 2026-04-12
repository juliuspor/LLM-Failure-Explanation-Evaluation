@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    parts = locale_str.split('_')
    if len(parts) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")
    language = parts[0]
    if len(language) != 2 or not language.islower() or not language.isalpha():
        raise ValueError(f"Invalid locale format: {locale_str}")
    if len(parts) == 1:
        return Locale(language, "")
    if len(parts) == 2:
        country = parts[1]
        if country == "":
            return Locale(language, "")
        if len(country) != 2 or not country.isupper() or not country.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country)
    # len(parts) >= 3: join any extra underscores into variant
    country = parts[1]
    variant = "_".join(parts[2:])
    if country == "":
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, "", variant)
    else:
        if len(country) != 2 or not country.isupper() or not country.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country, variant)