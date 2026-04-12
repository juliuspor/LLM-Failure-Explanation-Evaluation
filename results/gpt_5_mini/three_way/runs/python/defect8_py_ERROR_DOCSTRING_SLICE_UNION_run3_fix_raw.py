@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    # Split on underscores to handle cases like 'fr', 'en_GB', 'fr__POSIX', 'en_GB_VAR'
    parts = locale_str.split('_')
    if len(parts) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")

    language = parts[0]
    # Validate language: must be 2 lowercase letters
    if len(language) != 2 or not language.isalpha() or not language.islower():
        raise ValueError(f"Invalid locale format: {locale_str}")

    if len(parts) == 1:
        return Locale(language, "")
    elif len(parts) == 2:
        country = parts[1]
        if country == "":
            # empty country is allowed only if there's a variant (handled in >=3 parts)
            return Locale(language, "")
        # Validate country: must be 2 uppercase letters
        if len(country) != 2 or not country.isalpha() or not country.isupper():
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country)
    else:
        # 3 or more parts: language, country (may be empty), variant (rest joined with '_')
        country = parts[1]
        variant = '_'.join(parts[2:])
        if country != "":
            if len(country) != 2 or not country.isalpha() or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
        # variant must be non-empty
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country, variant)