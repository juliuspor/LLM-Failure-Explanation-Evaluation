@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    parts = locale_str.split('_')
    # Validate language
    if len(parts[0]) != 2 or not parts[0].islower() or not parts[0].isalpha():
        raise ValueError(f"Invalid locale format: {locale_str}")
    language = parts[0]

    # No more parts: just language
    if len(parts) == 1:
        return Locale(language, "")

    # Two parts: could be language_country or language_ (empty country)
    if len(parts) == 2:
        country = parts[1]
        if country == "":
            # Empty country treated as no country
            return Locale(language, "")
        # Validate country must be two uppercase letters
        if len(country) != 2 or not country.isalpha() or not country.isupper():
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country)

    # Three or more parts: language_country_variant or language__variant (empty country)
    # Recombine any extra underscores into variant
    country = parts[1]
    variant = "_".join(parts[2:])

    if country == "":
        # pattern language__variant
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, "", variant)
    else:
        # pattern language_country_variant
        if len(country) != 2 or not country.isalpha() or not country.isupper():
            raise ValueError(f"Invalid locale format: {locale_str}")
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country, variant)