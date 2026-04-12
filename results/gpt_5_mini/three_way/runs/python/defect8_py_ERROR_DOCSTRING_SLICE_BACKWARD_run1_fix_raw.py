@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    parts = locale_str.split('_')
    # Validate language
    if len(parts) == 0 or len(parts[0]) < 2 or len(parts[0]) > 3:
        raise ValueError(f"Invalid locale format: {locale_str}")
    language = parts[0]
    # language must be all lowercase letters
    if not language.isalpha() or not language.islower():
        raise ValueError(f"Invalid locale format: {locale_str}")

    # No more parts -> language only
    if len(parts) == 1:
        return Locale(language, "")

    # There is at least a country/empty part or variant
    country = parts[1]
    variant = ""
    if len(parts) > 2:
        # Variant is the remainder joined by underscore to preserve any underscores in variant
        variant = "_".join(parts[2:])

    # Validate country if present (allow empty for forms like 'fr__POSIX')
    if country:
        if len(country) != 2 or not country.isalpha() or not country.isupper():
            raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(language, country, variant)