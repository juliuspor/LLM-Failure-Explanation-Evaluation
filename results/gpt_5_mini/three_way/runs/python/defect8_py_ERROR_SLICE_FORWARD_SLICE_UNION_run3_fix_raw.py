@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    # Split into at most 3 parts: language, country, variant
    parts = locale_str.split('_', 2)
    if len(parts) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")

    language = parts[0]
    if len(language) != 2 or not language.islower() or not language.isalpha():
        raise ValueError(f"Invalid locale format: {locale_str}")

    country = ''
    variant = ''

    if len(parts) == 1:
        return Locale(language, country, variant)

    # parts length is 2 or 3
    country = parts[1]
    if len(parts) == 2:
        # Could be language_country or language__ (invalid if empty country)
        if country == '':
            # Trailing underscore with empty country is invalid
            raise ValueError(f"Invalid locale format: {locale_str}")
        if len(country) != 2 or not country.isupper() or not country.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country, variant)

    # len(parts) == 3
    variant = parts[2]
    # country may be empty (language__variant) or two uppercase letters
    if country == '':
        # empty country allowed when variant present
        if variant == '':
            # language__ (empty variant) is invalid
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, '', variant)
    else:
        if len(country) != 2 or not country.isupper() or not country.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        if variant == '':
            # language_country_ (empty variant) is invalid
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country, variant)