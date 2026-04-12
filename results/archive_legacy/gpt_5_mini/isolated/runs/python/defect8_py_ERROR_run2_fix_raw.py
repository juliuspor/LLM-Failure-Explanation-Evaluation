@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    parts = locale_str.split('_')
    if len(parts) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")
    language = parts[0]
    if len(language) != 2 or not (language.islower() and language.isalpha()):
        raise ValueError(f"Invalid locale format: {locale_str}")
    if len(parts) == 1:
        return Locale(language, "")
    if len(parts) == 2:
        part1 = parts[1]
        if len(part1) == 2 and part1.isupper() and part1.isalpha():
            return Locale(language, part1)
        else:
            raise ValueError(f"Invalid locale format: {locale_str}")
    # len(parts) >= 3
    if parts[1] == "":
        variant = "_".join(parts[2:])
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, "", variant)
    country = parts[1]
    if len(country) != 2 or not (country.isupper() and country.isalpha()):
        raise ValueError(f"Invalid locale format: {locale_str}")
    variant = "_".join(parts[2:])
    return Locale(language, country, variant)