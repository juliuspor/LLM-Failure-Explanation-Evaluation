@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    length = len(locale_str)
    if length == 2:
        if not (locale_str[0].isalpha() and locale_str[0].islower() and locale_str[1].isalpha() and locale_str[1].islower()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str, "")
    if length == 5:
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        lang = locale_str[0:2]
        country = locale_str[3:5]
        if not (lang[0].isalpha() and lang[0].islower() and lang[1].isalpha() and lang[1].islower()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if not (country[0].isalpha() and country[0].isupper() and country[1].isalpha() and country[1].isupper()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, country)
    if length >= 7:
        if locale_str[2] != '_' or locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        lang = locale_str[0:2]
        country = locale_str[3:5]
        variant = locale_str[6:]
        if not (lang[0].isalpha() and lang[0].islower() and lang[1].isalpha() and lang[1].islower()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if not (country[0].isalpha() and country[0].isupper() and country[1].isalpha() and country[1].isupper()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, country, variant)
    raise ValueError(f"Invalid locale format: {locale_str}")