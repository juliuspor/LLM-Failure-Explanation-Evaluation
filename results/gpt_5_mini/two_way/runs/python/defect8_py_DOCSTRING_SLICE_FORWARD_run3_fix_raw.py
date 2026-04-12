@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)

    # Language must be two lowercase letters
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Plain language (e.g., "en")
    if length == 2:
        return Locale(locale_str, "")

    # From here on, expect an underscore separator at position 2
    if length >= 3 and locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Language + country (e.g., "en_GB") requires total length == 5
    if length == 5:
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5])

    # Language + country + variant (e.g., "en_GB_xxx") requires at least 7 chars
    if length >= 7:
        # ensure second underscore at position 5
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[6:]
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5], variant)

    # Any other lengths are invalid
    raise ValueError(f"Invalid locale format: {locale_str}")