@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    # language must be 2 lowercase letters
    if len(locale_str) < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Split on underscores but keep empty parts (max 3 parts: language, country, variant)
    parts = locale_str.split('_', 2)

    # Validate language
    language = parts[0]
    if len(language) != 2 or not language.islower() or not language.isalpha():
        raise ValueError(f"Invalid locale format: {locale_str}")

    country = ''
    variant = ''

    if len(parts) == 1:
        return Locale(language, country, variant)

    # parts length >= 2
    country = parts[1]
    # Country, if present non-empty, must be 2 uppercase letters
    if country != '':
        if len(country) != 2 or not country.isalpha() or not country.isupper():
            raise ValueError(f"Invalid locale format: {locale_str}")

    if len(parts) == 2:
        return Locale(language, country, variant)

    # parts == 3 -> variant possibly empty? Require non-empty variant when underscore provided
    variant = parts[2]
    if variant == '':
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(language, country, variant)