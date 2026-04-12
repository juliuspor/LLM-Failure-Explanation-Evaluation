@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)

    # Language only: "ll"
    if length == 2:
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str, "")

    # Must have at least language + '_' + country => minimum length 5
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Common check: underscore after language
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Country-only or language_country: length ==5 -> en_US
    if length == 5:
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5])

    # length >= 7 expected form: ll_CC_variant where position 5 is '_'
    if length >= 7:
        # verify country letters at 3 and 4
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # verify underscore before variant
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[6:]
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5], variant)

    # Any other case is invalid
    raise ValueError(f"Invalid locale format: {locale_str}")