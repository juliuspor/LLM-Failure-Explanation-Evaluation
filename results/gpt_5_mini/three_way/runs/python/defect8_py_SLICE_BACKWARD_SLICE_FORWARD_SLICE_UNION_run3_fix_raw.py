@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    # Accept only underscore-separated formats like: ll, ll_CC, ll_CC_variant
    parts = locale_str.split('_')
    parts_count = len(parts)

    # Language mandatory and must be two lowercase letters
    if parts_count < 1 or len(parts[0]) != 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    language = parts[0]
    if not (language.isalpha() and language.islower()):
        raise ValueError(f"Invalid locale format: {locale_str}")

    # No more parts -> simple language locale
    if parts_count == 1:
        return Locale(language, "")

    # Country part must be exactly two uppercase letters
    country = parts[1]
    if len(country) != 2 or not (country.isalpha() and country.isupper()):
        raise ValueError(f"Invalid locale format: {locale_str}")

    if parts_count == 2:
        return Locale(language, country)

    # Variant exists: join remaining parts with '_'
    variant = '_'.join(parts[2:])
    if len(variant) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(language, country, variant)