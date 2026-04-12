@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    parts = locale_str.split('_')
    if len(parts) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # language part
    language = parts[0]
    if len(language) != 2 or not language.isalpha() or not language.islower():
        raise ValueError(f"Invalid locale format: {locale_str}")

    # no more parts -> language only
    if len(parts) == 1:
        return Locale(language, "")

    # country part (may be empty)
    country = parts[1]
    if country == "":
        # empty country allowed only if there is a variant following
        if len(parts) == 2:
            # trailing underscore with no variant is invalid
            raise ValueError(f"Invalid locale format: {locale_str}")
    else:
        if len(country) != 2 or not country.isalpha() or not country.isupper():
            raise ValueError(f"Invalid locale format: {locale_str}")

    # variant part (may contain underscores if more than 3 parts)
    if len(parts) == 2:
        return Locale(language, country)
    else:
        variant = '_'.join(parts[2:])
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country, variant)