@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    length = len(locale_str)
    if length == 2:
        lang = locale_str
        if len(lang) != 2 or not ('a' <= lang[0] <= 'z') or not ('a' <= lang[1] <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, "")
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")
    lang = locale_str[0:2]
    if not ('a' <= lang[0] <= 'z') or not ('a' <= lang[1] <= 'z'):
        raise ValueError(f"Invalid locale format: {locale_str}")
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    if locale_str[3] == '_':
        variant = locale_str[4:]
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, "", variant)
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if not ('A' <= ch3 <= 'Z') or not ('A' <= ch4 <= 'Z'):
        raise ValueError(f"Invalid locale format: {locale_str}")
    country = locale_str[3:5]
    if length == 5:
        return Locale(lang, country)
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    variant = locale_str[6:]
    if len(variant) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")
    return Locale(lang, country, variant)