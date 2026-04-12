@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    # Split by underscore to avoid fixed index access issues
    parts = locale_str.split('_')
    parts_count = len(parts)

    # Validate language part
    if parts_count < 1 or len(parts[0]) != 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    language = parts[0]
    if not (language[0].islower() and language[1].islower() and language.isalpha()):
        raise ValueError(f"Invalid locale format: {locale_str}")

    if parts_count == 1:
        return Locale(language, "")
    elif parts_count == 2:
        country = parts[1]
        # country must be exactly 2 uppercase letters
        if len(country) != 2 or not country.isalpha() or not (country[0].isupper() and country[1].isupper()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country)
    else:
        # parts_count >= 3 => language_country_variant (variant may contain underscores originally, so recombine)
        country = parts[1]
        variant = '_'.join(parts[2:])
        if len(country) != 2 or not country.isalpha() or not (country[0].isupper() and country[1].isupper()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country, variant)