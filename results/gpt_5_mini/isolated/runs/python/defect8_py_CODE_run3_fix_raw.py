@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # Accept form: ll | ll_CC | ll_CC_variant (where ll=2 lower, CC=2 upper, variant>=1)
    if not (length == 2 or length == 5 or length >= 7):
        raise ValueError(f"Invalid locale format: {locale_str}")

    # language: first two chars must be lowercase letters
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    lang = locale_str[0:2]
    if not (lang.isalpha() and lang.islower() and len(lang) == 2):
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 2:
        return Locale(lang, "")

    # must have '_' at position 2
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length >= 5:
        country = locale_str[3:5]
        if not (country.isalpha() and country.isupper() and len(country) == 2):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 5:
            return Locale(lang, country)

    # for length >=7 must have '_' at position 5 and a non-empty variant
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    variant = locale_str[6:]
    if len(variant) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")
    return Locale(lang, country, variant)