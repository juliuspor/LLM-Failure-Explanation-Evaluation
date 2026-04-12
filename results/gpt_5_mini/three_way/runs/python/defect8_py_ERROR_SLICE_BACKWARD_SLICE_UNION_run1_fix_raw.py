@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    # Normalize separators: allow '-' as well as '_'
    locale_str = locale_str.replace('-', '_')

    # Split into at most 3 parts: language, country, variant
    parts = locale_str.split('_', 2)

    if len(parts) == 0 or not parts[0]:
        raise ValueError(f"Invalid locale format: {locale_str}")

    language = parts[0]
    if len(language) != 2 or not language.isalpha():
        raise ValueError(f"Invalid locale format: {locale_str}")

    language = language.lower()

    # No country/variant
    if len(parts) == 1:
        return Locale(language, "")

    # parts has at least 2 elements: country may be empty (e.g., 'fr__POSIX')
    country = parts[1]
    variant = ""
    if len(parts) == 3:
        variant = parts[2]

    if country:
        if len(country) != 2 or not country.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = country.upper()
    else:
        country = ""

    return Locale(language, country, variant)