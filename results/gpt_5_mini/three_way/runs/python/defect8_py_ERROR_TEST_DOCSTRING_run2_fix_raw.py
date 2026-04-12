@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    parts = locale_str.split('_', 2)
    # parts can be: [language], [language, country], [language, country, variant]
    if len(parts) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")

    language = parts[0]
    if len(language) != 2 or not language.islower() or not language.isalpha():
        raise ValueError(f"Invalid locale format: {locale_str}")

    if len(parts) == 1:
        return Locale(language, "")

    # parts[1] may be country or empty string (for empty country with variant)
    country = parts[1]
    variant = ""
    if len(parts) == 3:
        variant = parts[2]

    if country == "":
        # empty country allowed only if there's a variant
        if variant == "":
            # form like 'en_' or 'en__' without variant is invalid
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, "", variant)
    else:
        # country must be exactly 2 uppercase letters
        if len(country) != 2 or not country.isalpha() or not country.isupper():
            raise ValueError(f"Invalid locale format: {locale_str}")
        if variant == "":
            return Locale(language, country)
        else:
            return Locale(language, country, variant)