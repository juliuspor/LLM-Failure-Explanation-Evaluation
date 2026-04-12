@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    # Accept separators '_' as per Java Locale.toString format
    parts = locale_str.split('_')

    # At minimum we need language
    if len(parts) == 0 or len(parts[0]) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")

    language = parts[0]
    # language must be 2 lowercase letters (ISO 639)
    if len(language) != 2 or not language.isalpha() or language.lower() != language:
        raise ValueError(f"Invalid locale format: {locale_str}")

    country = ""
    variant = ""

    if len(parts) == 1:
        return Locale(language, country, variant)
    elif len(parts) == 2:
        # Could be language_country or language__variant (empty country)
        if parts[1] == "":
            # Empty country, no variant
            return Locale(language, "", "")
        # country must be 2 uppercase letters
        country_candidate = parts[1]
        if len(country_candidate) != 2 or not country_candidate.isalpha() or country_candidate.upper() != country_candidate:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country_candidate, "")
    else:
        # len(parts) >= 3 -> language_country_variant or language__variant
        country_candidate = parts[1]
        variant_candidate = "_".join(parts[2:])  # variant may contain underscores

        if country_candidate == "":
            # Accept empty country, variant must be non-empty
            if len(variant_candidate) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, "", variant_candidate)
        else:
            # Validate country
            if len(country_candidate) != 2 or not country_candidate.isalpha() or country_candidate.upper() != country_candidate:
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(variant_candidate) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country_candidate, variant_candidate)