@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    if length == 2:
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str, "")

    # For lengths other than 2, must be at least 5 (lang_COUNTRY) or >=7 (lang_COUNTRY_variant)
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # positions 0-1 must be lowercase letters
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # position 2 must be underscore
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Now length >=5, safe to access 3 and 4
    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # length > 5: must have '_' at position 5 and at least one variant char after
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length < 7:
        # Need at least one variant character
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])