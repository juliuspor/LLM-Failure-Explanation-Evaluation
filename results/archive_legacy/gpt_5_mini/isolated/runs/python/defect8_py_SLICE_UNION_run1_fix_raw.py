@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    length = len(locale_str)
    if length == 2:
        lang = locale_str
        if len(lang) != 2 or not lang.isalpha() or not lang.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, "")
    if length == 5:
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        lang = locale_str[0:2]
        country = locale_str[3:5]
        if not (len(lang) == 2 and lang.isalpha() and lang.islower()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if not (len(country) == 2 and country.isalpha() and country.isupper()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, country)
    if length >= 7:
        if locale_str[2] != '_' or locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        lang = locale_str[0:2]
        country = locale_str[3:5]
        variant = locale_str[6:]
        if not (len(lang) == 2 and lang.isalpha() and lang.islower()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if not (len(country) == 2 and country.isalpha() and country.isupper()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, country, variant)
    raise ValueError(f"Invalid locale format: {locale_str}")