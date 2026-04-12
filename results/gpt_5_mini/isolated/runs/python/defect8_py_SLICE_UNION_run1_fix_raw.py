@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    # Split into at most 3 parts: language, country, variant
    parts = locale_str.split('_', 2)

    # Validate language
    if len(parts[0]) != 2 or not parts[0].islower() or not parts[0].isalpha():
        raise ValueError(f"Invalid locale format: {locale_str}")

    language = parts[0]

    if len(parts) == 1:
        return Locale(language, "")
    elif len(parts) == 2:
        country = parts[1]
        # Country must be exactly 2 uppercase letters
        if len(country) != 2 or not country.isalpha() or not country.isupper():
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country)
    else:
        # len(parts) == 3
        country = parts[1]
        variant = parts[2]
        if len(country) != 2 or not country.isalpha() or not country.isupper():
            raise ValueError(f"Invalid locale format: {locale_str}")
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country, variant)