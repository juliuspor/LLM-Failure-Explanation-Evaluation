@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    parts = locale_str.split('_')
    # Validate language
    if len(parts[0]) != 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch0 = parts[0][0]
    ch1 = parts[0][1]
    if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Only language
    if len(parts) == 1:
        return Locale(parts[0], "")

    # Language and country (or empty country with variant)
    country = parts[1]
    if country != "":
        if len(country) != 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = country[0]
        ch4 = country[1]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")

    # No variant
    if len(parts) == 2:
        return Locale(parts[0], country)

    # Variant present
    variant = '_'.join(parts[2:])
    if variant == "":
        raise ValueError(f"Invalid locale format: {locale_str}")
    return Locale(parts[0], country, variant)