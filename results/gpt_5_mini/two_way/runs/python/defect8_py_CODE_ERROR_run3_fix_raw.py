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

    country = ""
    variant = ""

    if len(parts) >= 2:
        country = parts[1]
    if len(parts) == 3:
        variant = parts[2]

    # When only language is present
    if country == "" and variant == "":
        return Locale(language, "", "")

    # If country present (could be empty when variant exists like 'fr__POSIX')
    if country:
        if len(country) != 2 or not country.isupper() or not country.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
    else:
        # empty country is allowed only if variant is present
        if variant == "":
            # e.g., 'en_' or 'en__' are invalid
            raise ValueError(f"Invalid locale format: {locale_str}")

    # If variant present, it must be non-empty
    if variant != "":
        return Locale(language, country, variant)
    else:
        return Locale(language, country)