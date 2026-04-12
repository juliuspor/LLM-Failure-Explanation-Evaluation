@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # Valid forms: ll, ll_CC, ll_CC_V (variant length >=1)
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # validate language (positions 0-1)
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
        raise ValueError(f"Invalid locale format: {locale_str}")

    # language only
    if length == 2:
        return Locale(locale_str, "")

    # must have '_' after language
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # must have at least two chars for country (positions 3 and 4)
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")

    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if not ('A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
        raise ValueError(f"Invalid locale format: {locale_str}")

    # language + country
    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # must have '_' before variant
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # variant must be non-empty
    if length <= 6:
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])