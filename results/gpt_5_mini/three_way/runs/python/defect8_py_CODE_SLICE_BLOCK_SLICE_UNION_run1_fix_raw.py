@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # Accept forms: ll, ll_CC, ll_CC_variant (where ll = 2 letters, CC = 2 letters, separators are '_')
    if length != 2 and length != 5 and length < 7:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # language: first two chars must be letters
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    lang = locale_str[0:2]
    if not (lang.isalpha() and len(lang) == 2):
        raise ValueError(f"Invalid locale format: {locale_str}")

    # normalize language to lower-case
    lang = lang.lower()

    if length == 2:
        return Locale(lang, "")

    # expecting underscore at pos 2
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")

    country = locale_str[3:5]
    if not (country.isalpha() and len(country) == 2):
        raise ValueError(f"Invalid locale format: {locale_str}")
    country = country.upper()

    if length == 5:
        return Locale(lang, country)

    # length >= 7: expect '_' at pos 5 and variant after pos 6
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    variant = locale_str[6:]
    if variant == "":
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(lang, country, variant)