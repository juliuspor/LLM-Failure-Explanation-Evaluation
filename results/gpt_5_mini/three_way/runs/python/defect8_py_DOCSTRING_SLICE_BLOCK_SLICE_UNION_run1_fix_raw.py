@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # valid minimal forms: 2 (language), 5 (language_country), or >=7 (language_country_variant)
    if length == 2:
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str, "")

    # For longer forms, must have '_' at position 2
    if length < 5 or locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Now safe to check country characters at 3 and 4
    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # length >=6: expect '_' at position 5 and variant thereafter
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # variant may be any length >=1 (since length >=7 expected for a non-empty variant)
    if length == 6:
        # underscore present but no variant
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])