@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    # Split into at most 3 parts: language[_country][_variant]
    parts = locale_str.split('_', 2)
    # parts length can be 1,2 or 3
    if len(parts) == 1:
        lang = parts[0]
        if len(lang) != 2 or not lang.islower() or not lang.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, "")

    # len(parts) >= 2
    lang = parts[0]
    country = parts[1]
    variant = parts[2] if len(parts) == 3 else ""

    # Validate language
    if len(lang) != 2 or not lang.islower() or not lang.isalpha():
        raise ValueError(f"Invalid locale format: {locale_str}")

    # If there are exactly 2 parts and the second part is a 2-letter country
    if len(parts) == 2:
        if len(country) == 0:
            # Form like "ll_" is invalid
            raise ValueError(f"Invalid locale format: {locale_str}")
        if len(country) == 2 and country.isupper() and country.isalpha():
            return Locale(lang, country)
        else:
            # Could be language + variant without country (invalid form), reject
            raise ValueError(f"Invalid locale format: {locale_str}")

    # len(parts) == 3
    # country may be empty (i.e., original string was 'll__variant')
    if country == "":
        # variant must be non-empty
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, "", variant)
    else:
        # country present: must be 2 uppercase letters
        if len(country) != 2 or not country.isupper() or not country.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, country, variant)