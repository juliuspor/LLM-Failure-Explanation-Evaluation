@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # Accept forms: ll, ll_CC, ll_CC_variant (variant may be empty but separator must exist)
    if not (length == 2 or length == 5 or length >= 7):
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Validate language (two lowercase letters)
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    lang = locale_str[0:2]
    if not (lang.isalpha() and lang[0].islower() and lang[1].islower()):
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 2:
        return Locale(lang, "")

    # Must have '_' at position 2
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")

    country = locale_str[3:5]
    if not (country.isalpha() and country[0].isupper() and country[1].isupper()):
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 5:
        return Locale(lang, country)

    # length >= 7: must have '_' at position 5 and variant follows
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    variant = locale_str[6:]
    return Locale(lang, country, variant)