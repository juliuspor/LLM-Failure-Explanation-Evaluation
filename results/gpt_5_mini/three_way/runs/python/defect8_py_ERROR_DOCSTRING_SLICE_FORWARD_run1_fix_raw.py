@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    parts = locale_str.split('_')
    # Valid forms: language; language_country; language_country_variant
    if len(parts) == 0 or len(parts) > 3:
        raise ValueError(f"Invalid locale format: {locale_str}")

    language = parts[0]
    # language must be exactly 2 lowercase letters
    if len(language) != 2 or not language.isalpha() or not language.islower():
        raise ValueError(f"Invalid locale format: {locale_str}")

    if len(parts) == 1:
        return Locale(language, "")

    country = parts[1]
    # country must be exactly 2 uppercase letters
    if len(country) != 2 or not country.isalpha() or not country.isupper():
        raise ValueError(f"Invalid locale format: {locale_str}")

    if len(parts) == 2:
        return Locale(language, country)

    # len(parts) == 3
    variant = parts[2]
    if len(variant) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(language, country, variant)